# Generated by Django 4.0.5 on 2022-07-12 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0023_folder_breadcrumb_html_folder_folder_tree_html_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='breadcrumb_html',
        ),
        migrations.RemoveField(
            model_name='folder',
            name='folder_tree_html',
        ),
        migrations.RemoveField(
            model_name='normalnotes',
            name='breadcrumb_html',
        ),
    ]
