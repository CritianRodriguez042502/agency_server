# Generated by Django 4.2.4 on 2023-10-23 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0002_remove_model_users_img_model_users_url_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model_users',
            name='url_img',
        ),
        migrations.AddField(
            model_name='model_users',
            name='img',
            field=models.ImageField(blank=True, upload_to='img_users'),
        ),
    ]
