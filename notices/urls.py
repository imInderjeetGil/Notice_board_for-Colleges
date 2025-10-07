from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import StudentNoticeListView, AllNoticesListView,NoticeCreateView,NoticeUpdateView, NoticeDeleteView, NoticeDetailView,MyNoticesListView, SubscribeView,create_admin

urlpatterns = [
  
    path('', views.StudentNoticeListView.as_view(), name='notice-list'), 
    path('create-notice/', NoticeCreateView.as_view(), name='create-notice'),
    path('<int:pk>/edit/', NoticeUpdateView.as_view(), name='notice-update'),
    path('<int:pk>/delete/', NoticeDeleteView.as_view(), name='notice-delete'),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
    path('archive/', AllNoticesListView.as_view(), name='notice-archive'),
    path('my-notices/', MyNoticesListView.as_view(), name='my-notices'),
    path('about/', TemplateView.as_view(template_name='notices/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='notices/contact.html'), name='contact'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path("create-admin/", create_admin, name="create_admin"),
]