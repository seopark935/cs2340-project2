from django import forms
from .models import JobSeeker

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = [
            "firstName",
            "lastName",
            "location",
            "image",
            "education",
            "degree",
            "startYear",
            "endYear",
            "headline",
            "experience",
            "skills",
        ]
        widgets = {
            "headline": forms.Textarea(attrs={"rows": 3}),
            "experience": forms.CheckboxSelectMultiple,
            "skills": forms.CheckboxSelectMultiple,
        }
