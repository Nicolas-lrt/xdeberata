from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'content']


class CommentLoggedForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']