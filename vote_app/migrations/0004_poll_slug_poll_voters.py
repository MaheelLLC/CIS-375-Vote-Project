# Generated by Django 5.0.6 on 2024-07-16 00:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0003_poll_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='slug',
            field=models.SlugField(default='default-slug', max_length=200),
        ),
        migrations.AddField(
            model_name='poll',
            name='voters',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]