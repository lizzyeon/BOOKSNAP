from django.urls import path
from .views import UploadFeed, MySnap

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('mysnap', MySnap.as_view())
]
