from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Note, Tag


# TODO: Improve or handle post request for action into separate view.
class HomeView(View):
    """
    Home view to handle get, post methods.
    """

    template_name = "index.html"

    # overriding dispatch method to add authentication
    def dispatch(self, request, *args, **kwargs):
        # check if user is logged in
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    # get HTTP method
    def get(self, request, *args, **kwargs):
        # get notes from database
        all_notes = Note.published.filter(user=request.user)
        # filter unpinned notes
        notes = all_notes.filter(pinned=False)
        # filter pinned notes
        pinned_notes = all_notes.filter(pinned=True)

        # create context variable
        context = {
            "notes": notes,
            "pinned_notes": pinned_notes,
        }

        return render(request, self.template_name, context)

    # post HTTP method
    def post(self, request, note_id, *args, **kwargs):
        # get note based on note id
        note = Note.published.get(pk=note_id)

        # get actions
        actions = request.POST

        # handle actions
        if "pinned" in actions:
            note.pinned = not note.pinned
        if "archived" in actions:
            note.archived = not note.archived

        # save the object
        note.save()

        return redirect("home")


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


class DraftsView(LoginRequiredMixin, TemplateView):
    template_name = "drafts.html"

    # set context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get drafts
        drafts = Note.objects.filter(user=self.request.user).filter(status="DF")

        # set context
        context["drafts"] = drafts

        return context


class ArchiveView(LoginRequiredMixin, TemplateView):
    template_name = "archive.html"

    # set context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get archived
        archives = Note.objects.filter(user=self.request.user).filter(archive=True)

        # set context
        context["archives"] = archives

        return context


class TagsView(LoginRequiredMixin, TemplateView):
    template_name = "tags.html"

    # set context data
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # get tags
        tags = Tag.objects.all()

        # set context
        context["tags"] = tags

        return context
