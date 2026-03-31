from django.contrib import admin
from .models import Feed, Like, Reply, Bookmark, Follow

admin.site.register(Feed)
admin.site.register(Like)
admin.site.register(Reply)
admin.site.register(Bookmark)
admin.site.register(Follow)