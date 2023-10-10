from django.shortcuts import render

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
