# Generated by Django 5.0.4 on 2024-04-10 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_answer_author_alter_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(null=True),
        ),
    ]