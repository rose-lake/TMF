# Generated by Django 2.2.9 on 2020-02-07 23:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TMF', '0008_remove_article_publish_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(related_name='articles', to='TMF.Author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 7, 23, 1, 30, 803157, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='TMF.Article')),
            ],
        ),
    ]
