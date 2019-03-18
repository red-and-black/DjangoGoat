from django import forms

from .models import Note


class WriteNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content', 'receiver')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
