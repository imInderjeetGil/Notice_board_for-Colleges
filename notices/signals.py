# signals.py - Push notification signals disabled
# Using custom notification system in views.py instead

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from webpush import send_group_notification
# from .models import Notice

# @receiver(post_save, sender=Notice)
# def notify_all_students(sender, instance, created, **kwargs):
#     if created:
#         payload = {
#             "title": "New Notice Posted!",
#             "body": instance.title,
#             "url": f"/notices/{instance.id}/"
#         }
#         send_group_notification(group_name="students", payload=payload, ttl=1000)
