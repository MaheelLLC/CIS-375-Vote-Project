# Generated by Django 5.0.6 on 2024-07-14 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0002_remove_poll_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='user',
            field=models.CharField(default='', max_length=200),
        ),
    ]