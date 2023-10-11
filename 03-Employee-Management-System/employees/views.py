from django.shortcuts import render


def home(request):
    return render(request, "employees/index.html", {})


def add(request):
    return render(request, "employees/add_employee.html", {})
