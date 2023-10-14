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
    employee_form = EmployeeForm(initial={"gender": ""})

    # handle POST request
    if request.method == "POST":
        # create a HTML form with POST data
        employee_form = EmployeeForm(request.POST)
        education_form = EducationForm(request.POST)

        # validate employee and education form and create data base object
        if employee_form.is_valid() and education_form.is_valid():
            employee = Employee(
                first_name=employee_form.cleaned_data["first_name"],
                middle_name=employee_form.cleaned_data["middle_name"],
                last_name=employee_form.cleaned_data["last_name"],
                age=employee_form.cleaned_data["age"],
                gender=employee_form.cleaned_data["gender"],
                email=employee_form.cleaned_data["email"],
                phone=employee_form.cleaned_data["phone"],
                designation=employee_form.cleaned_data["designation"],
                education=Education.objects.create(
                    institute_name=education_form.cleaned_data["institute_name"],
                    degree_title=education_form.cleaned_data["degree_title"],
                    field_of_study=education_form.cleaned_data["field_of_study"],
                    start_date=education_form.cleaned_data["start_date"],
                    end_date=education_form.cleaned_data["end_date"],
                    grade=education_form.cleaned_data["grade"],
                    description=education_form.cleaned_data["description"],
                ),
            )
            employee.save()

        # redirect to employee detail page
        return redirect(reverse("employee_detail", args=[employee.id]))

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

    # dictionary for pre populating form with initial data.
    initial_employee_data = {
        # employee information
        "first_name": employee.first_name,
        "middle_name": employee.middle_name,
        "last_name": employee.last_name,
        "age": employee.age,
        "gender": employee.gender,
        "email": employee.email,
        "phone": employee.phone,
        "designation": employee.designation,
    }
    initial_education_data = {
        # education information
        "institute_name": employee.education.institute_name,
        "degree_title": employee.education.degree_title,
        "field_of_study": employee.education.field_of_study,
        "start_date": employee.education.start_date,
        "end_date": employee.education.end_date,
        "grade": employee.education.grade,
        "description": employee.education.description,
    }
    employee_form = EmployeeForm(initial=initial_employee_data)
    education_form = EducationForm(initial_education_data)

    # if POST request is sent
    if request.method == "POST":  # or request.POST
        # create a HTML form with POST data
        employee_form = EmployeeForm(request.POST)
        education_form = EducationForm(request.POST)

        # validate employee and education form and update the related database object
        if employee_form.is_valid() and education_form.is_valid():
            # update employee object fields
            employee.first_name = employee_form.cleaned_data["first_name"]
            employee.middle_name = employee_form.cleaned_data["middle_name"]
            employee.last_name = employee_form.cleaned_data["last_name"]
            employee.age = employee_form.cleaned_data["age"]
            employee.gender = employee_form.cleaned_data["gender"]
            employee.email = employee_form.cleaned_data["email"]
            employee.phone = employee_form.cleaned_data["phone"]
            employee.designation = employee_form.cleaned_data["designation"]
            employee.save()

            # get education object related to employee
            education = Education.objects.get(id=employee.education.id)

            # update education object fields
            education.institute_name = education_form.cleaned_data["institute_name"]
            education.degree_title = education_form.cleaned_data["degree_title"]
            education.field_of_study = education_form.cleaned_data["field_of_study"]
            education.start_date = education_form.cleaned_data["start_date"]
            education.end_date = education_form.cleaned_data["end_date"]
            education.grade = education_form.cleaned_data["grade"]
            education.description = education_form.cleaned_data["description"]
            education.save()

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
