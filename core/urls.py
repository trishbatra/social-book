from django.urls import path
from . import views
appname = "core"
urlpatterns = [
    path("" , views.index, name="index"),
    path("signup/" , views.signup, name="signup"),
    path("signin/" , views.signin, name="signin"),
    path("logout/" , views.logout, name="logout"),
    path("search/" , views.search, name="search"),
    path("profile/<str:pk>" , views.profilez, name="profile"),
    path("settings/" , views.settings, name="settings"),
    path("upload/" , views.upload, name="upload"),
    path("like-post/" , views.like_post, name="like-post"),
    path("follow/" , views.follow, name="follow"),
]
