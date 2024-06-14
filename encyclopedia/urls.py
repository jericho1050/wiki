from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("search/search_results", views.search, name="results"),
    path("create/", views.create_new, name="create_new"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("random/", views.random, name="random")
]
