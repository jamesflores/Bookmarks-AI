from django.urls import path

from .views import *


urlpatterns = [
    path("", HomePageView, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("app/", BookmarksView, name="bookmarks"),
    path("app/category/<str:category>/", BookmarksView, name="category"),
    path("app/add/", add_bookmark, name="add_bookmark"),
    path("app/edit/<int:pk>/", edit_bookmark, name="edit_bookmark"),
    path("app/delete/<int:pk>/", delete_bookmark, name="delete_bookmark"),
]
