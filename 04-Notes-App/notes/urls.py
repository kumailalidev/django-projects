from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
]
