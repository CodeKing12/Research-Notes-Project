# Generated by Django 4.0.5 on 2022-07-11 14:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0021_alter_folder_folder_dict'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='normalnotes',
            name='date_created',
        ),
        migrations.AlterField(
            model_name='normalnotes',
            name='date_modified',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
        ),
    ]
