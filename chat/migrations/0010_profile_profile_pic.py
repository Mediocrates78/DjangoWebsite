# Generated by Django 4.0.4 on 2022-11-05 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='avatar.svg', null=True, upload_to='images/profile/'),
        ),
    ]
