from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "location",
            "remote_type",
            "salary_min",
            "salary_max",
            "visa_sponsorship",
            "skills",
        ]
