# Generated by Django 4.2.1 on 2023-05-20 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(default='default_cover.jpg', upload_to=''),
        ),
    ]
