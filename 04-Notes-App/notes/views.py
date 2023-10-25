from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Note, Tag


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
        note = Note.objects.get(pk=note_id)

        # get actions
        actions = request.POST

        # handle actions
        if "pinned" in actions:
            # change the pinned status
            note.pinned = not note.pinned

            # pinned notes cannot be archived
            note.archived = False
        if "archived" in actions:
            note.archived = not note.archived

            # archived notes cannot be pinned
            note.pinned = False

        # save the object
        note.save()

        return redirect("home")


class UserRegistrationView(CreateView):
    template_name = "registration/user_registration_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class NoteCreateView(LoginRequiredMixin, CreateView):
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


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = "_update_form"  # default is "_form"
    model = Note
    fields = "__all__"
    success_url = "/"


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    # template_name = "note_confirm_delete" # default
    model = Note
    success_url = reverse_lazy("home")


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
        archives = Note.objects.filter(user=self.request.user).filter(archived=True)

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


class TagCreateView(View):
    """
    View for creating tag. Only HTTP POST method is allowed.
    """

    template_name = "notes/tag_create_form.html"

    # adding authentication
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    # handling HTTP GET request
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    # handling HTTP POST request
    def post(self, request, *args, **kwargs):
        # get the tag name
        name = request.POST.get("name")

        if name:
            # create and save tag object into database
            tag = Tag(name=name)
            tag.save()
            return redirect("tags")

        return render(request, self.template_name)


class TagDeleteView(View):
    """
    View for deleting a tag. Only HTTP POST and GET method are allowed.
    """

    template_name = "notes/tag_confirm_delete.html"

    # adding authentication
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    # handling HTTP GET request
    def get(self, request, pk):
        # get tag object
        tag = get_object_or_404(Tag, pk=pk)

        return render(request, self.template_name, {"object": tag})

    # HTTP delete method
    def delete(self, request, pk):
        # get tag object
        tag = get_object_or_404(Tag, pk=pk)

        # delete tag object
        tag.delete()

        return redirect("tags")

    # handling HTTP POST method
    def post(self, request, pk):
        return self.delete(request, pk)


class TagUpdateView(View):
    """
    View for updating tag. Only HTTP GET, POST and UPDATE methods are allowed.
    """

    template_name = "notes/tag_update_form.html"

    # adding authentication
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        # get tag object
        tag = get_object_or_404(Tag, pk=pk)

        return render(request, self.template_name, {"tag": tag})

    def post(self, request, pk):
        # get tag object
        tag = get_object_or_404(Tag, pk=pk)

        # get updated tag name
        name = request.POST.get("name")

        if name:
            # update the tag name
            tag.name = name
            tag.save()
            return redirect("tags")

        return render(request, self.template_name, {"tag": tag})
