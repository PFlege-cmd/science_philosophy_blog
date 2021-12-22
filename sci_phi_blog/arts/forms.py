import django.forms as forms;
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Article, Picture, Response


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text','language','category','snippet','background_picture']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ResponseForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
    #    self.user_to_add = kwargs.pop('user_to_add', None)
    #    print("Popped a kwarg")
     #   super(ResponseForm, self).__init__(**kwargs)

    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


