# Generated by Django 2.2.4 on 2019-12-13 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20191212_0259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='answers',
            new_name='module',
        ),
        migrations.RenameField(
            model_name='quizitem',
            old_name='answers',
            new_name='module',
        ),
    ]
