# Generated by Django 4.0.5 on 2022-07-03 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_folder_path_folder_subfiles_folder_subfolders_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='parent',
        ),
        migrations.AddField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='notes.folder'),
        ),
    ]
