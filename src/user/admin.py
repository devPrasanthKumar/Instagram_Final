from django.contrib import admin

# Register your models here.

from .models import Profile, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "username", "created_at", "update_at")
    search_fields = ("user", "bio", "location")
    list_filter = ("user", "username")
    list_display_links = ("user", "username")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "followed", "created_at", "updated_on")
    search_fields = ("user__username", "followed__username")
    list_filter = ("user", "followed")
    list_display_links = ("user", "followed")
