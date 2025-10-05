# notices/attachment_forms.py

from django import forms
from django.forms.models import inlineformset_factory
from .models import Notice, Attachment

# 1. Form for a single attachment
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        # Notice is excluded because it's set automatically by the Formset
        fields = ['file', 'name'] 
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional file description'}),
        }

# 2. Formset factory to handle multiple attachments for one notice
# extra=3 means 3 empty file upload fields will show by default
AttachmentFormSet = inlineformset_factory(
    parent_model=Notice, 
    model=Attachment, 
    form=AttachmentForm, 
    fields=['file', 'name'], 
    extra=3, 
    can_delete=True
)