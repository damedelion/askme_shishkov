# Generated by Django 5.0.4 on 2024-05-08 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_answer_rating_answer_likes_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='img/img.jpg'),
        ),
    ]