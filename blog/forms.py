"""Blog comment form."""

from django import forms
from .models import BlogComment


class BlogCommentForm(forms.ModelForm):
    """Comment form for blog posts."""

    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
            }),
        }
