from django.contrib import admin
from .models import Feed, Like, Reply, Bookmark, Follow
from django.utils.html import format_html


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('content', 'image_preview', 'email')
    search_fields = ('email', 'content')
    ordering = ('-id',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="/media/{}" width="80" height="80" style="object-fit:cover;" />',
                obj.image
            )
        return "-"

    image_preview.short_description = 'Image'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('feed_id', 'email', 'is_like')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('feed_id', 'email', 'reply_content')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('feed_id', 'email', 'is_marked')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'is_followed')
    search_fields = ('from_user__email', 'to_user__email')
    list_filter = ('is_followed',)
