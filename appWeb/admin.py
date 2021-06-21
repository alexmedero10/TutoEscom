from django.contrib import admin
from .models import Post, Profile, Relationship, Like, Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Relationship)
admin.site.register(Like)
admin.site.register(Comment)