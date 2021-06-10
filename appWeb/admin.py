from django.contrib import admin
from .models import Post, Profile, Relationship, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Relationship)
admin.site.register(Like)