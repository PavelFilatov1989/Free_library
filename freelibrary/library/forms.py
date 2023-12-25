from django import forms
from .models import Category

class AddBookForm(forms.Form):
    author = forms.CharField(max_length=255)
    book = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())