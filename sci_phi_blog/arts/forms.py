import django.forms as forms;
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Article, Picture

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text','language','background_picture']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }

