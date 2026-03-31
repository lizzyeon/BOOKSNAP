from django.contrib import admin
from .models import Feed, Like, Reply, Bookmark, Follow

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feed')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feed')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feed')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feed')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user')