# Generated by Django 4.2.5 on 2023-09-23 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_followerscount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followerscount',
            old_name='followedBy',
            new_name='user',
        ),
    ]
