from .views import Join, Login, LogOut
from django.urls import path

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view())

]