from django import forms
from .models import JobSeeker, Skill

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
            "experience": forms.Textarea(attrs={"rows": 5}),  # ✅ text area for job history
            "skills": forms.TextInput(attrs={"placeholder": "e.g. Python, Django, SQL"}),          # ✅ many-to-many checkbox
        }

