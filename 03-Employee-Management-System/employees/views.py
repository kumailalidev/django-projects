from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Employee, Education
from .forms import EducationForm, EmployeeForm


def home(request):
    employees = Employee.objects.all()

    # handle GET request
    if request.GET:
        # get sorting parameter value
        sort_by = request.GET.get("sort_by")

        # mapping sorting parameters
        SORT_BY_MAPPING = {
            "name_asc": "first_name",
            "name_dsc": "-first_name",
            "age_asc": "age",
            "age_dsc": "-age",
            "dob_asc": "date_of_birth",
            "dob_dsc": "-date_of_birth",
        }

        # sort queryset by sort_by value
        if sort_by in SORT_BY_MAPPING:
            employees = employees.order_by(SORT_BY_MAPPING[sort_by])

    return render(request, "employees/index.html", {"employees": employees})


def search(request):
    if request.method == "GET":  # or request.GET
        # get search URL parameter
        search_text = request.GET.get("query")  # returns None if does not exists

        # filter employees by __str__ representation (inefficient)
        # TODO: Update filtering using Q objects
        if search_text != "" and search_text is not None:
            # get all the employees from database
            employees = Employee.objects.all()

            # filter employees
            employees = [
                employee
                for employee in employees
                if search_text in str(employee).lower()
            ]
            return render(
                request,
                "employees/search_results.html",
                {"search_text": search_text, "employees": employees},
            )
        else:
            return redirect("home")

    return redirect("home")


def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)

    return render(request, "employees/employee_detail.html", {"employee": employee})


def add(request):
    # Create education form
    education_form = EducationForm()
    employee_form = EmployeeForm()

    # handle POST request
    if request.method == "POST":
        # create a from instance from POST data.
        employee_form = EmployeeForm(request.POST)
        education_form = EducationForm(request.POST)

        # validate employee and education form and create data base object
        if employee_form.is_valid() and education_form.is_valid():
            # Create an employee database object, but don't save
            employee_obj = employee_form.save(commit=False)

            # Create and save education database object
            education_obj = education_form.save()

            # Modify the education OneToOne field of an employee object
            employee_obj.education = education_obj

            # Save the updated database object
            employee_obj.save()

        # redirect to employee detail page
        return redirect(reverse("employee_detail", args=[employee_obj.id]))

    return render(
        request,
        "employees/add_employee.html",
        {
            "education_form": education_form,
            "employee_form": employee_form,
        },
    )


def update_employee(request, id):
    # get the employee object
    employee = get_object_or_404(Employee, id=id)

    # Create a employee and education form instance with a prepopulated data
    employee_form = EmployeeForm(instance=employee)
    education_form = EducationForm(instance=employee.education)

    # if POST request is sent
    if request.method == "POST":
        # create a form instance with POST data
        employee_form = EmployeeForm(request.POST, instance=employee)
        education_form = EducationForm(request.POST, instance=employee.education)

        # validate employee and education form and update the related database object
        if employee_form.is_valid() and education_form.is_valid():
            # Update the employee and education database instance
            employee_form.save()
            education_form.save()
            # NOTE:
            # save() method returns the updated instance by default and this behavior
            # can be suppress by overriding the save method of ModelForm.

            # redirect to employee details
            return redirect(reverse("employee_detail", args=[employee.id]))

    context = {
        "education_form": education_form,
        "employee_form": employee_form,
    }

    return render(request, "employees/update_employee.html", context)


def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()

    return redirect("home")
