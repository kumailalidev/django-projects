from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<int:note_id>/", views.HomeView.as_view(), name="home"),
    path("drafts/", views.DraftsView.as_view(), name="drafts"),
    path("archive/", views.ArchiveView.as_view(), name="archive"),
    path("tags/", views.TagsView.as_view(), name="tags"),
    # Notes
    path("note/create/", views.NoteCreateView.as_view(), name="create_note"),
    path("note/<int:pk>/update/", views.NoteUpdateView.as_view(), name="update_note"),
    path("note/<int:pk>/delete/", views.NoteDeleteView.as_view(), name="delete_note"),
    # Tags
    path("tag/create/", views.TagCreateView.as_view(), name="create_tag"),
    path("tag/<int:pk>/delete/", views.TagDeleteView.as_view(), name="delete_tag"),
    # Login and Registration
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password_rest/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "accounts/register/",
        views.UserRegistrationView.as_view(),
        name="register",
    ),
]
