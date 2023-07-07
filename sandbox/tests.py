from django.test import TestCase

# Create your tests here.

from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
# end CommentForm

f = CommentForm()
f
