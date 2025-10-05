import os
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

NOTICE_TYPES = [
    ('Common', 'Common'),
    ('Examinations', 'Examinations'),
    ('Assignments', 'Assignments'),
    ('Notes', 'Notes'),
    ('Events', 'Events'),
    ('Backs', 'Backs'),
    ('Urgent', 'Urgent'),
]

DEPARTMENTS=[
    ('CSE', 'Computer Science and Engineering'),
    ('EE', 'Electrical Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
]

SEMESTERS=[
    ('S1', 'Semester 1'),
    ('S2', 'Semester 2'),
    ('S3', 'Semester 3'),
    ('S4', 'Semester 4'),
    ('S5', 'Semester 5'),
    ('S6', 'Semester 6'),
    ('S7', 'Semester 7'),
    ('S8', 'Semester 8'),
    ('ALL', 'All Semesters'),
]

class Notice(models.Model):
    title = models.CharField(max_length=200)

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    notice_type = models.CharField(max_length=50, choices=NOTICE_TYPES, default='Common')

    department = models.CharField(max_length=50, choices=DEPARTMENTS, default='CSE')
    semester = models.CharField(max_length=50, choices=SEMESTERS, default='ALL')

    description = models.TextField()

    def filename(self):
        if self.attachment:
            return os.path.basename(self.attachment.name)
        return None 
    
    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.title
    
class Attachment(models.Model):
    # The file itself
    file = models.FileField(upload_to='notice_attachments/multiple/')
    
    # The link back to the parent notice (ForeignKey)
    notice = models.ForeignKey(Notice, related_name='attachments', on_delete=models.CASCADE)
    
    # Optional: A user-friendly name for the file
    name = models.CharField(max_length=100, blank=True) 

    def filename(self):
        import os
        return os.path.basename(self.file.name)
    
    def __str__(self):
        return f"{self.name or self.filename()} attached to {self.notice.title}"
    
class PushSubscription(models.Model):
    # The unique URL/identifier for the browser's service worker
    endpoint = models.URLField(max_length=500, unique=True)
    
    # Key fields required by the Push API
    p256dh_key = models.CharField(max_length=100)
    auth_key = models.CharField(max_length=100)
    
    # Optional: Link to a user if they are logged in (for personalized filtering)
    # Since students don't log in, this is set to null=True
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Filtering preferences (so we only notify on relevant notices)
    department = models.CharField(max_length=3, choices=DEPARTMENTS, default='ALL')
    semester = models.CharField(max_length=3, choices=SEMESTERS, default='ALL')
    
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.endpoint[:30]}..."

    class Meta:
        verbose_name = "Push Subscription"
        verbose_name_plural = "Push Subscriptions"

