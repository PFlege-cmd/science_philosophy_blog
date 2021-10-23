import django.forms as forms;
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Article, Picture

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text','language','background_picture']

