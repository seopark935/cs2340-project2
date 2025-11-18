from django.urls import path
from .views import (
    signup_choice,
    jobseeker_signup,
    recruiter_signup,
    RoleLoginView,
    logout_view,
    recommendation_settings,
    export_recruiters_csv,
)

urlpatterns = [
    path("signup/", signup_choice, name="signup.choice"),
    path("signup/jobseeker/", jobseeker_signup, name="signup.jobseeker"),
    path("signup/recruiter/", recruiter_signup, name="signup.recruiter"),
    path("map/jobseeker/", recruiter_signup, name="map.index"),
    path("login/", RoleLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("settings/recommendations/", recommendation_settings, name="accounts.recommendation_settings"),
    path("export/recruiters/", export_recruiters_csv, name="accounts.export_recruiters"),
]

