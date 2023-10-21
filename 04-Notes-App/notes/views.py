from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.contrib.auth.forms import UserCreationForm


class HomeView(View):
    template_name = "index.html"

    # handle GET request
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {})


class UserRegistrationView(generic.CreateView):
    template_name = "registration/user_registration_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
