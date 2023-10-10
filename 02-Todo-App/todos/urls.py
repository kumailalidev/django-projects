from django.urls import path

from todos import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_todo, name="add_todo"),
    path("delete/<int:id>/", views.delete_todo, name="delete_todo"),
]
