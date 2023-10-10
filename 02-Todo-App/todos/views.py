from django.http import Http404
from django.shortcuts import redirect, render

from .models import Todo


def home(request):
    """
    View to handle homepage and search functionality
    """
    todos = Todo.objects.all()
    incomplete_todos = todos.filter(completed=False).count()

    # handle search and sorting functionality
    if request.GET:
        # get search and sorting parameter
        search_title = request.GET.get("title")
        sort_by = request.GET.get("sort_by")

        # dictionary to map sort_by values to field names for ordering
        SORT_BY_MAPPING = {
            "ascending": "title",
            "descending": "-title",
            "date_created": "-created_at",
            "date_updated": "-updated_at",
        }

        # filter todos only if title is not empty
        if search_title:
            todos = todos.filter(title__icontains=search_title)
            context = {
                "todos": todos,
                "search_title": search_title,
            }

            # render search template
            return render(request, "todos/search.html", context)

        # sort todos
        if sort_by in SORT_BY_MAPPING:
            # get the corresponding field name for mapping
            order_by_field = SORT_BY_MAPPING[sort_by]
            # apply the ordering to the queryset
            todos = todos.order_by(order_by_field)

    # context variable
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
