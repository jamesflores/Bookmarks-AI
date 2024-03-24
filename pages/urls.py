from django.urls import path

from .views import *


urlpatterns = [
    path("", HomePageView, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("app/", BookmarksView, name="bookmarks"),
    path("app/add/", add_bookmark, name="add_bookmark"),
]