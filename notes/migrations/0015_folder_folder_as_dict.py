# Generated by Django 4.0.5 on 2022-07-07 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0014_normalnotes_date_created_normalnotes_date_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='folder_dict',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
