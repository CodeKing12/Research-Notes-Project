# Generated by Django 4.0.5 on 2022-07-05 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0011_citations_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citations',
            name='month',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='citations',
            name='year',
            field=models.CharField(max_length=50),
        ),
    ]