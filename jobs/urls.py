from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="jobs.list"),
    path("dashboard/", views.job_dashboard, name="jobs.dashboard"),
    path("create/", views.job_create, name="jobs.create"),
    path("<int:pk>/edit/", views.job_edit, name="jobs.edit"),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]
