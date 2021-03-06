# Generated by Django 2.2.9 on 2020-01-30 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('byline', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=300)),
                ('uuid', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('byline', models.CharField(max_length=300)),
                ('created', models.DateTimeField()),
                ('disclosure', models.TextField()),
                ('headline', models.CharField(max_length=300)),
                ('modified', models.DateTimeField()),
                ('path', models.CharField(max_length=300)),
                ('promo', models.TextField()),
                ('uuid', models.CharField(max_length=300)),
                ('authors', models.ManyToManyField(to='TMF.Author')),
            ],
        ),
    ]
