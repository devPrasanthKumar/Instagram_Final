# Generated by Django 4.2.7 on 2023-12-08 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0009_alter_comment_options_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]