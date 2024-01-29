from django.contrib import admin

# Register your models here.
from .models import Post, Like, Comment

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display =[""]
