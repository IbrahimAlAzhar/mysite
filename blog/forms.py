from django import forms
from .models import Comment


class EmailPostForm(forms.Form): # post through email
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # using model Comment and override it using some attributes
        fields = ('name', 'email', 'body') # override these fields from model
