from django.contrib import admin

from .models import Comment, Like, News

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(News)
