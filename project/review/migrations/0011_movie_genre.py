# Generated by Django 2.1.2 on 2018-12-17 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_auto_20181217_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='', max_length=100),
        ),
    ]
