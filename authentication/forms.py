from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio')
        widgets = {
            'avatar': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 5}),
        }
