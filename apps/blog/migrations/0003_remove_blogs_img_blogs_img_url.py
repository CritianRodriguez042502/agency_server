# Generated by Django 4.2.4 on 2023-10-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogs',
            name='img',
        ),
        migrations.AddField(
            model_name='blogs',
            name='img_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
