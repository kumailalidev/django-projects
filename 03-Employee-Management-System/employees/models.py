from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True, null=True, max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    designation = models.CharField(max_length=250)


class Education(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="educations"
    )
    institute_name = models.CharField(max_length=250)
    degree_title = models.CharField(max_length=250)
    field_of_study = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
