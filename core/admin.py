from django.contrib import admin
from .models import Profile, Post, likePost, followersCount, addComment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(likePost)
admin.site.register(followersCount)
admin.site.register(addComment)