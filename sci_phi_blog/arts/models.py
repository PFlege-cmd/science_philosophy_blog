from django.core.validators import MinLengthValidator
from django.db import models
from enum import IntEnum

from accs.models import Account

class Languages(IntEnum):
    ENGLISH = 1
    DUTCH = 2
    FRENCH = 3
    GERMAN = 4
    JAPANESE = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Article(models.Model):
    title = models.CharField(null=False,
                             max_length=250,
                             validators=[MinLengthValidator(3, "Title must be at least three characters!")]
                             )
    text = models.TextField(null=False, blank=False)
    time_created = models.DateTimeField(verbose_name="time created", auto_now_add=True)
    last_edited = models.DateTimeField(verbose_name="last edited", auto_now=True)
    author = models.ForeignKey(Account, related_name="articles", on_delete=models.CASCADE)
    language = models.IntegerField(choices=Languages.choices(), default=Languages.ENGLISH)
    background_picture = models.ImageField(null = True, blank=True, upload_to='images/')


class Picture(models.Model):

    description = models.CharField(validators=[MinLengthValidator(5, "Please enter at least five characters!")],
                                   max_length=250)
    image = models.BinaryField(null = False)
    content_type = models.CharField(max_length=256, null=True, help_text="The MIMEType of the file")


