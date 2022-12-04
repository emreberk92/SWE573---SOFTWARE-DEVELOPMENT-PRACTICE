# Generated by Django 4.1.3 on 2022-12-01 13:27

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=50)),
                ('photo', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('creation_time', models.DateTimeField(default=datetime.datetime.now)),
                ('nr_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]