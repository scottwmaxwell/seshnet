# Generated by Django 4.0.4 on 2022-04-27 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_pic',
            new_name='image',
        ),
    ]
