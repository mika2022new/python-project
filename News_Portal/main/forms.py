from django import forms
from .models import Post

from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):

    content = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title == content:
            raise ValidationError(
                "Заголовок не должен быть идентичным контенту."
            )

        return cleaned_data