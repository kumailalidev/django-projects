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
