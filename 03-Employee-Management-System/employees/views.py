from django.shortcuts import redirect, render, get_object_or_404

from .models import Employee, Education


def home(request):
    employees = Employee.objects.all()

    # handle GET request
    if request.GET:
        # get search parameter
        search_text = request.GET.get("search")

        # filter employees by __str__ representation (inefficient)
        # TODO: Update filtering using Q objects
        employees = [
            employee for employee in employees if search_text in str(employee).lower()
        ]

    return render(request, "employees/index.html", {"employees": employees})


def add(request):
    # if POST request is sent
    if request.method == "POST":  # or request.POST
        # get URL parameters
        # basic info
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        date_of_birth = request.POST.get("date_of_birth")
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
        employee = Employee.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            age=age,
            date_of_birth=date_of_birth,
            email=email,
            phone=phone,
            designation=designation,
        )

        # Create education object
        education = Education(
            employee=employee,
            institute_name=institute_name,
            degree_title=degree_title,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            grade=grade,
            description=description,
        )
        education.save()

        return redirect("home")

    return render(request, "employees/add_employee.html")


def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)

    return render(request, "employees/employee_detail.html", {"employee": employee})
