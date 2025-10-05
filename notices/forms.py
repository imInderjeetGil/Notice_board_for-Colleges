from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    # This inner class tells the ModelForm what model to use and which fields to include
    class Meta:
        model = Notice
        # We exclude 'posted_by' and 'posted_at' because they will be set automatically in the view.
        fields = ['title', 'notice_type', 'department', 'semester', 'description']
        
        # Optional: Add Bootstrap classes to the fields for better styling
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'notice_type': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }