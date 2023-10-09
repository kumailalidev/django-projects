from django.urls import path

from todos import views

urlpatterns = [
    path("", views.home, name="home"),
]
