# Generated by Django 2.1.2 on 2018-10-30 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='firstview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstview_text', models.CharField(max_length=200)),
                ('rating', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.TextField(default='')),
                ('plot', models.TextField(default='')),
                ('runtime', models.TextField(default='')),
                ('rated', models.TextField(default='Unknown')),
                ('title', models.TextField(default='')),
                ('year', models.IntegerField(default=1900)),
            ],
        ),
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=200)),
                ('rating', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='firstview',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.Movie'),
        ),
    ]
