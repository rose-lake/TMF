# Generated by Django 2.2.9 on 2020-02-03 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TMF', '0004_auto_20200203_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='created',
            new_name='publish_at',
        ),
    ]
