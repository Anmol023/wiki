from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new, name = "new_page"),
    path("wiki/<str:name>", views.title, name = "title"),
    path("search", views.search, name="search"),
    path("wiki/<str:name>/edit", views.edit, name = "edit"),
    path("random", views.random, name = "random")
]
