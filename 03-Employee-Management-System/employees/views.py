from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Employee, Education


def home(request):
    employees = Employee.objects.all()

    # handle GET request
    if request.GET:
        # get search parameter
        search_text = request.GET.get("search")

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

        # filter employees by __str__ representation (inefficient)
        # TODO: Implement search functionality in separate view
        # TODO: Update filtering using Q objects
        if search_text != "" and search_text is not None:
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

        # sort queryset by sort_by value
        if sort_by in SORT_BY_MAPPING:
            employees = employees.order_by(SORT_BY_MAPPING[sort_by])

    return render(request, "employees/index.html", {"employees": employees})


def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)

    return render(request, "employees/employee_detail.html", {"employee": employee})


def add(request):
    # if POST request is sent
    if request.method == "POST":  # or request.POST
        # get URL parameters

        # basic info
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        designation = request.POST.get("designation")

        # education
        institute_name = request.POST.get("institute_name")
        degree_title = request.POST.get("degree_title")
        field_of_study = request.POST.get("field_of_study")
        start_date = request.POST.get("start_date")
        end_date = (
            request.POST.get("end_date") if request.POST.get("end_date") else None
        )
        grade = request.POST.get("grade")
        description = request.POST.get("description")

        # create employee object

        # Create education and employee objects
        education = Education(
            institute_name=institute_name,
            degree_title=degree_title,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            grade=grade,
            description=description,
        )
        education.save()

        employee = Employee.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            age=age,
            gender=gender,
            email=email,
            phone=phone,
            designation=designation,
            education=education,
        )
        employee.save()

        return redirect("home")

    return render(request, "employees/add_employee.html")


def update_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    # if POST request is sent
    if request.method == "POST":  # or request.POST
        # get education object related to employee
        education = Education.objects.get(id=employee.education.id)

        # update employee object fields
        employee.first_name = request.POST.get("first_name")
        employee.middle_name = request.POST.get("middle_name")
        employee.last_name = request.POST.get("last_name")
        employee.age = request.POST.get("age")
        employee.gender = request.POST.get("gender")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")
        employee.designation = request.POST.get("designation")
        employee.save()

        # update education object fields
        education.institute_name = request.POST.get("institute_name")
        education.degree_title = request.POST.get("degree_title")
        education.field_of_study = request.POST.get("field_of_study")
        education.start_date = request.POST.get("start_date")
        education.end_date = (
            request.POST.get("end_date") if request.POST.get("end_date") else None
        )
        education.grade = request.POST.get("grade")
        education.description = request.POST.get("description")
        education.save()

        # redirect to employee details
        return redirect(reverse("employee_detail", args=[employee.id]))

    return render(request, "employees/update_employee.html", {"employee": employee})


def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()

    return redirect("home")
