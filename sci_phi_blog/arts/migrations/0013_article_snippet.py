# Generated by Django 3.2.3 on 2021-10-31 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arts', '0012_alter_article_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='snippet',
            field=models.CharField(default='Click above to read post', max_length=255),
        ),
    ]