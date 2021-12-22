from django.core.validators import MinLengthValidator
from django.db import models
from enum import Enum
from ckeditor.fields import RichTextField

from accs.models import Account
from django.urls import reverse_lazy


class Languages(Enum):
    ENGLISH = 'English'
    DUTCH = 'Nederlands'
    FRENCH = 'Français'
    GERMAN = 'Deutsch'
    JAPANESE = '日本'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Categories(Enum):
    GENERAL = 'General';
    PHILOSPHY = 'Philosophy'
    SCIENCE = 'Science'
    PSYCHOLOGY = 'Psychology'
    PRODUCTIVITY = 'Productivity'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def lang_choice(cls, lang: str) -> bool:
        if lang in cls.value:
            return True
        else:
            return False


class Article(models.Model):
    title = models.CharField(null=False,
                             max_length=250,
                             validators=[MinLengthValidator(3, "Title must be at least three characters!")]
                             )
    #text = models.TextField(null=False, blank=False)
    text = RichTextField(null=True, blank=True)
    time_created = models.DateTimeField(verbose_name="time created", auto_now_add=True)
    last_edited = models.DateTimeField(verbose_name="last edited", auto_now=True)
    author = models.ForeignKey(Account, related_name="articles", on_delete=models.CASCADE)
    language = models.CharField(choices=Languages.choices(), default=Languages.ENGLISH, max_length=100)
    category = models.CharField(choices=Categories.choices(), default=Categories.GENERAL, max_length=50)
    background_picture = models.ImageField(null = True, blank=True, upload_to='images/')
    responses = models.ManyToManyField(Account, through='Response', related_name="responded_to")
    snippet = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse_lazy("arts:article", kwargs={'pk':self.pk});


class Picture(models.Model):

    description = models.CharField(validators=[MinLengthValidator(5, "Please enter at least five characters!")],
                                   max_length=250)
    image = models.BinaryField(null = False)
    content_type = models.CharField(max_length=256, null=True, help_text="The MIMEType of the file")

class Response(models.Model):
    body = models.TextField(null=False, blank=False)
    time_created = models.DateTimeField(verbose_name="time created", auto_now_add=True)
    last_edited = models.DateTimeField(verbose_name="last edited", auto_now=True)
    author = models.ForeignKey(Account, related_name="responses", null=False, on_delete=models.CASCADE)
    response_to_response = models.ForeignKey('self', related_name="responded_by", null=True, on_delete=models.CASCADE)
    response_to_article = models.ForeignKey(Article, related_name="response_comments", on_delete=models.CASCADE)



