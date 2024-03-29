# Generated by Django 4.0.5 on 2022-07-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citations',
            options={'verbose_name': 'citation'},
        ),
        migrations.AlterModelOptions(
            name='folder',
            options={'verbose_name': 'folder'},
        ),
        migrations.AlterModelOptions(
            name='normalnotes',
            options={'verbose_name': 'note'},
        ),
        migrations.AlterModelOptions(
            name='papers',
            options={'verbose_name': 'paper'},
        ),
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name': 'tag'},
        ),
        migrations.AddField(
            model_name='normalnotes',
            name='path',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='normalnotes',
            name='slug',
            field=models.SlugField(default='', max_length=600),
        ),
    ]
