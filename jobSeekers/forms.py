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
            "years_experience",
            "open_to_work",
            "desired_salary_min",
            "desired_salary_max",
            "education",
            "degree",
            "startYear",
            "endYear",
            "headline",
            "hide_profile",
            "hide_image",
            "hide_headline"
        ]
        widgets = {
            "headline": forms.Textarea(attrs={"rows": 3}),
            'open_to_work': forms.CheckboxInput(),
            'hide_location': forms.CheckboxInput(),
            'hide_image': forms.CheckboxInput(),
            'hide_headline': forms.CheckboxInput(),
            'hide_profile': forms.CheckboxInput()
        }

        labels = {
            'hide_image': "Keep your image private",
            'hide_headline': "Keep your headline private",
            'hide_profile': "Keep profile hidden"
        }

