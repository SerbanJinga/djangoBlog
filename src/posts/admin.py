from django.contrib import admin

# Register your models here.
from .models import Author, Comment, Post, Category, Tag

admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)