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
            "hide_profile",
            "hide_image",
            "hide_headline"
        ]
        widgets = {
            "headline": forms.Textarea(attrs={"rows": 3}),
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

