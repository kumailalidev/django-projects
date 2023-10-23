from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm

from .models import Note


class HomeView(TemplateView):
    template_name = "index.html"

    # set context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # published notes
        notes = Note.published.filter(user=self.request.user)
        context["notes"] = notes

        return context

    # override dispatch method to check whether user is logged in or not
    # NOTE: This can be achieved using LoginRequiredMix class as base class.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    template_name = "registration/user_registration_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class NoteCreateView(CreateView):
    template_name_suffix = "_create_form"  # default is "_form"
    model = Note
    fields = [
        "title",
        "body",
        "status",
    ]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # set user value to current logged in user
        form.instance.user = self.request.user

        return super().form_valid(form)
