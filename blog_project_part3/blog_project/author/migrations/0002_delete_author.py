# Generated by Django 4.2.10 on 2024-02-16 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_author'),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
    ]
