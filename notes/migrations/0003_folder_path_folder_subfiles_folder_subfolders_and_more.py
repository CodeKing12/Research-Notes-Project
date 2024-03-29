# Generated by Django 4.0.5 on 2022-07-03 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_citations_options_alter_folder_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='path',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folder',
            name='subfiles',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folder',
            name='subfolders',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type',
            name='subfiles',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type',
            name='subfolders',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
    ]
