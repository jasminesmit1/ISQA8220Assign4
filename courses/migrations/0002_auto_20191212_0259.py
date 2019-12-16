# Generated by Django 2.2.4 on 2019-12-12 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model_in': ('text', 'video', 'image', 'file', 'quizitem')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]