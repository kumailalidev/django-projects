from django import forms


class EducationForm(forms.Form):
    institute_name = forms.CharField(label="Institute Name", max_length=250)
    degree_title = forms.CharField(label="Degree Title", max_length=250)
    field_of_study = forms.CharField(label="Field of Study", max_length=50)
    start_date = forms.DateField(
        label="Start Date", widget=forms.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateField(
        label="End Date", widget=forms.DateInput(attrs={"type": "date"})
    )
    grade = forms.CharField(label="Grade", max_length=10)
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={"placeholder": "Enter short description of your degree."}
        ),
    )


class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age = forms.IntegerField()
    gender = forms.ChoiceField(
        choices=(
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other"),
            ("", "Select your gender"),  # Selected as default
        )
    )
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    designation = forms.CharField(max_length=250)
