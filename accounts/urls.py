from django.urls import path
from .views import signup_choice, jobseeker_signup, recruiter_signup, RoleLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", signup_choice, name="signup.choice"),
    path("signup/jobseeker/", jobseeker_signup, name="signup.jobseeker"),
    path("signup/recruiter/", recruiter_signup, name="signup.recruiter"),

    path("login/", RoleLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
