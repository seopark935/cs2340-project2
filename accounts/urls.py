from django.urls import path
from .views import signup_choice, jobseeker_signup, recruiter_signup, RoleLoginView, logout_view

urlpatterns = [
    path("signup/", signup_choice, name="signup.choice"),
    path("signup/jobseeker/", jobseeker_signup, name="signup.jobseeker"),
    path("signup/recruiter/", recruiter_signup, name="signup.recruiter"),

    path("login/", RoleLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),  # ✅ use custom view
]
