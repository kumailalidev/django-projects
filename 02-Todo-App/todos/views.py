from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Todo


def home(request):
    """
    home view function to display list of todo objects.
    """
    todos = Todo.objects.all()
    incomplete_todos = todos.filter(completed=False).count()

    context = {
        "todos": todos,
        "incomplete_todos": incomplete_todos,
    }

    return render(request, "todos/index.html", context)


def add_todo(request):
    """
    View to handle functionality of adding a todo
    """

    if request.POST:
        title = request.POST.get("title")

        # Create todo object only if todo title is not empty
        if title:
            Todo.objects.create(title=title)
            return redirect("home")
        else:
            return redirect("home")
    # if user try to access /add/
    else:
        return redirect("home")
