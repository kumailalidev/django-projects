from django.shortcuts import render

from .models import Todo


def home(request):
    """
    home view function to display list of todo objects.
    """
    todos = Todo.objects.all()
    context = {
        "todos": todos,
    }

    return render(request, "todos/index.html", context)
