from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photo', default='blank_photo') # No photo available at the moment
    location = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    creation_time = models.DateTimeField(default=datetime.now)
    nr_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class likePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class followersCount(models.Model):
    follower = models.CharField(max_length=50)
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.user
