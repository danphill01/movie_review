# Generated by Django 2.1.2 on 2018-12-07 17:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20181113_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='last_reviewed',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last reviewed'),
            preserve_default=False,
        ),
    ]
