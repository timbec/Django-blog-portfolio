# Generated by Django 3.0.1 on 2020-01-23 20:24

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20191219_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
