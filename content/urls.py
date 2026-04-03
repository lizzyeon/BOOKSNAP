from django.urls import path
from .views import UploadFeed, MySnap, feed_detail, Main, UploadReply, ToggleLike, ToggleBookmark, ToggleFollow



urlpatterns = [
    path('upload/', UploadFeed.as_view()),
    path('mysnap/<str:nickname>/', MySnap.as_view(), name='mysnap'),
    path('feed_detail/', feed_detail),
    path('main/', Main.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('follow/', ToggleFollow.as_view()),
]
