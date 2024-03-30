from django.urls import path

from .views import *


urlpatterns = [
    path("", HomePageView, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("privacy/", PrivacyPageView.as_view(), name="privacy_policy"),
    path("terms-of-service/", TermsOfServicePageView.as_view(), name="terms_of_service"),
    path("app/", BookmarksView, name="bookmarks"),
    path("app/category/<str:category>/", BookmarksView, name="category"),
    path("app/add/", add_bookmark, name="add_bookmark"),
    path("app/edit/<int:pk>/", edit_bookmark, name="edit_bookmark"),
    path("app/delete/<int:pk>/", delete_bookmark, name="delete_bookmark"),
    path("app/search/", SearchBookmarksView, name="search_bookmarks"),
]
