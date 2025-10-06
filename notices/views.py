# notices/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q # Used to create 'OR' logic
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404,redirect
from .models import PushSubscription,Notice
from .forms import NoticeForm
from .attachment_forms import AttachmentFormSet
from django.utils import timezone
from django.views import View # <-- NEW IMPORT
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from webpush.utils import _send_notification


def vapid_key(request):
    return {'vapid_key': settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY']}

@method_decorator(csrf_exempt, name='dispatch')
class SubscribeView(View):
    def post(self, request, *args, **kwargs):
        try:
            # 1. Parse the JSON data sent from the browser
            data = json.loads(request.body)
            endpoint = data.get('endpoint')
            keys = data.get('keys', {})
            
            if not endpoint:
                return JsonResponse({'status': 'error', 'message': 'Missing endpoint'}, status=400)
            
            # Extract the necessary keys
            p256dh = keys.get('p256dh')
            auth = keys.get('auth')
            
            if not p256dh or not auth:
                return JsonResponse({'status': 'error', 'message': 'Missing push keys'}, status=400)
            
            # 2. Extract filtering preferences (we can assume default filters for now)
            # A future step could allow the student to select filters on a settings page
            
            # 3. Create or Update the subscription record
            # We use update_or_create to handle returning students
            subscription, created = PushSubscription.objects.update_or_create(
                endpoint=endpoint,
                defaults={
                    'p256dh_key': p256dh,
                    'auth_key': auth,
                    # We can hardcode 'ALL' for default filtering for now
                    'department': 'ALL',
                    'semester': 'ALL',
                    # 'user': request.user if request.user.is_authenticated else None,
                }
            )

            message = 'Subscription created successfully' if created else 'Subscription updated successfully'
            return JsonResponse({'status': 'ok', 'message': message}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # Log the error (optional)
            print(f"Subscription error: {e}")
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)



class MyNoticesListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/my_notices.html' # NEW TEMPLATE
    context_object_name = 'notices'
    
    # Filter the queryset to only include notices posted by the current user
    def get_queryset(self):
        return Notice.objects.filter(posted_by=self.request.user).order_by('-posted_at')

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        notice = self.get_object()
        return notice.posted_by == self.request.user

    def handle_no_permission(self):
        return redirect('notice-list')

class NoticeUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/notice_form.html'
    
    # Add the Attachment Formset to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # For POST: Bind to the data, and instance is the current object
            context['attachment_formset'] = AttachmentFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            # For GET: Display Formset linked to the current object's attachments
            context['attachment_formset'] = AttachmentFormSet(instance=self.object)
        return context

    # Process both forms on successful submission
    def form_valid(self, form):
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']
        
        if attachment_formset.is_valid():
            # Save the main Notice object
            self.object = form.save()
            
            # Save the Formset (This updates/deletes/creates attachments)
            attachment_formset.instance = self.object
            attachment_formset.save()
            
            return super().form_valid(form)
        else:
            # If formset is invalid, return the form with errors
            return self.render_to_response(self.get_context_data(form=form))

    # Add this line if you haven't already
    def get_success_url(self):
        return reverse('notice-detail', kwargs={'pk': self.object.pk})

class NoticeDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Notice
    template_name = 'notices/notice_confirm_delete.html' 
    success_url = reverse_lazy('notice-list')
    context_object_name = 'notice' 

class StudentNoticeListView(ListView):
    model = Notice
    # Django will look for this file: notices/templates/notices/notice_list.html
    template_name = 'notices/notice_list.html' 
    context_object_name = 'notices'

    def get_queryset(self):
        department_filter = self.request.GET.get('department')
        search_query = self.request.GET.get('search')

        queryset = Notice.objects.all().order_by('-posted_at')
    
       
        if department_filter or search_query:
            # Filters notices where the department field matches the selection
            if department_filter:
                queryset = queryset.filter(department=department_filter)

        # 4. Apply Search Filter (Title, Description, or Posted By name)
            if search_query:
                # Use Q objects for OR logic: search in title OR description OR username
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(posted_by__username__icontains=search_query)
                )
        else:
            today = timezone.localdate()
            queryset = queryset.filter(posted_at__date=today).order_by('-posted_at')
        return queryset

class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/notice_form.html'
    success_url = reverse_lazy('notice-list')

    # Add the Attachment Formset to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # If POST request, bind the Formset data
            context['attachment_formset'] = AttachmentFormSet(self.request.POST, self.request.FILES)
        else:
            # If GET request, display blank Formset
            context['attachment_formset'] = AttachmentFormSet()
        return context


    def send_notice_push(self, notice):
        # 1. Prepare the payload (what the student's browser will display)
        payload = {
            "title": f"New Notice: {notice.get_department_display()}",
            "body": notice.title,
            "url": reverse('notice-detail', kwargs={'pk': notice.pk}) # Link to the new notice
        }

        # 2. Get all relevant subscriptions based on filters
        # For simplicity, we are currently only filtering by those who subscribed to 'ALL'
        subscriptions = PushSubscription.objects.filter(
             # In a future update, this would filter by notice.department and notice.semester
             # For now, let's notify everyone who is subscribed (or if they have 'ALL' selected)
             Q(department='ALL') | Q(department=notice.department)
        ).distinct()

        # 3. Send the notification to each active subscription
        sent_count = 0
        failed_count = 0
        
        for subscription in subscriptions:
            # webpush expects the full subscription object, not just the token
            try:
                # 'send_user_notification' is a slight misnomer; it sends to the subscription
                _send_notification(
                    user=None, # Not using Django User, so set to None
                    subscription_object=subscription,
                    payload=payload,
                    ttl=1000 # Time to Live (seconds)
                )
                sent_count += 1
                print(f"Successfully sent notification to {subscription.endpoint[:30]}...")
            except Exception as e:
                failed_count += 1
                # Log the error and delete the token if it's expired
                print(f"Failed to send notification to endpoint {subscription.endpoint}: {e}")
                # Uncomment the next line to automatically clean up bad tokens
                # subscription.delete()
        
        print(f"Push notification summary: {sent_count} sent, {failed_count} failed")

    # Process both forms on successful submission
    def form_valid(self, form):
        # 1. Set the user before saving the Notice form
        form.instance.posted_by = self.request.user
        
        # 2. Get the attachment formset from the context
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']
        
        # 3. Check if the formset data is valid
        if attachment_formset.is_valid():
            # Save the main Notice object
            self.object = form.save()
            
            # Link the Formset to the saved Notice object and save attachments
            attachment_formset.instance = self.object
            attachment_formset.save()
            self.send_notice_push(self.object)

            return super().form_valid(form)
        else:
            # If formset is invalid, return the form with errors
            return self.render_to_response(self.get_context_data(form=form))
    

    
class NoticeDetailView(DetailView):
    model = Notice
    # Django will automatically look for notices/notice_detail.html
    template_name = 'notices/notice_detail.html'
    context_object_name = 'notice'

class AllNoticesListView(ListView):
    model = Notice
    # Django will look for this file: notices/templates/notices/notice_list.html
    template_name = 'notices/all_notices_archive.html' 
    context_object_name = 'notices'

    def get_queryset(self):
        department_filter = self.request.GET.get('department')
        search_query = self.request.GET.get('search')
        semester_filter = self.request.GET.get('semester')
        queryset = Notice.objects.all().order_by('-posted_at')
    
        # Apply Department Filter
        if department_filter:
            queryset = queryset.filter(department=department_filter)

        if semester_filter and semester_filter != 'ALL':
            queryset = queryset.filter(semester=semester_filter)
        # Apply Search Filter (using Q logic)
        if search_query:
            queryset = queryset.filter(
                # Existing search fields (Title, Description, Posted By)
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(posted_by__username__icontains=search_query) |
                
                # NEW: Search the Attachment model's fields
                Q(attachments__name__icontains=search_query) |        # Search the custom name given by the teacher
                Q(attachments__file__icontains=search_query)          # Search the actual filename/path
            ).distinct() # Use .distinct() to prevent duplicate notices if multiple attachments match

        return queryset