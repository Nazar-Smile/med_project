from django.contrib import admin

# Register your models here.

from apps.blog.models import Category, Post

admin.site.register(Category)
admin.site.register(Post)


