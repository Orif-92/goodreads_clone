# Generated by Django 4.2.1 on 2023-05-19 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to=''),
        ),
    ]
