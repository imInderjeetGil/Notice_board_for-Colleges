# notices/context_processors.py

from django.conf import settings

def vapid_key(request):
    # This function returns the public key from settings, which Django/webpush expects
    return {
        'vapid_key': settings.WEBPUSH_SETTINGS.get('VAPID_PUBLIC_KEY')
    }