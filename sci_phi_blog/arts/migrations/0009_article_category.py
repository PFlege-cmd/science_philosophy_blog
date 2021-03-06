# Generated by Django 3.2.3 on 2021-10-28 04:01

import arts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arts', '0008_alter_article_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('General', 'GENERAL'), ('Philosophy', 'PHILOSPHY'), ('Science', 'SCIENCE'), ('Psychology', 'PSYCHOLOGY'), ('Productivity', 'PRODUCTIVITY')], default=arts.models.Categories['GENERAL'], max_length=50),
        ),
    ]
