from django import forms
from .models import Comments, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'content']


class CommentLoggedForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']


class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'main_img', 'bodyPreview', 'body']

        # widget = {
        #     'main_img': forms.FileInput(attrs={'required': 'required'}),
        # }
    # main_img.widget.attrs['required'] = 'required'