from django.db import models


class Education(models.Model):
    institute_name = models.CharField(max_length=250)
    degree_title = models.CharField(max_length=250)
    field_of_study = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)


class Employee(models.Model):
    # gender choices as a list of tuples
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    # basic information
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True, null=True, max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="O")
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    designation = models.CharField(max_length=250)

    # education
    education = models.OneToOneField(
        Education,
        on_delete=models.SET_NULL,
        related_name="education_details",
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}"
