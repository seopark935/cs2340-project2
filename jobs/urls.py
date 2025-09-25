from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="jobs.list"),
    path("create/", views.job_create, name="jobs.create"),
    path("<int:pk>/edit/", views.job_edit, name="jobs.edit"),
]
