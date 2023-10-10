from django.http import Http404
from django.shortcuts import redirect, render

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


def delete_todo(request, id):
    """
    View to handle delete functionality of a todo.
    """
    try:
        todo = Todo.objects.get(id=id)
        todo.delete()
        return redirect("home")
    except Todo.DoesNotExist:
        raise Http404("Todo object does not exists...")


def update_todo(request, id):
    """
    View to handle update functionality of todo
    """
    # get todo object
    try:
        todo = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        raise Http404("Todo object does not exists...")

    # if user updates the todo
    if request.POST:
        # getting values
        title = request.POST.get("title")
        completed = True if request.POST.get("completed") == "on" else False

        # updating todo object
        todo.title = title
        todo.completed = completed
        todo.save()

        return redirect("home")

    return render(request, "todos/update_todo.html", {"todo": todo})
