from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="jobs.list"),
    path("dashboard/", views.job_dashboard, name="jobs.dashboard"),
    path("create/", views.job_create, name="jobs.create"),
    path("<int:pk>/edit/", views.job_edit, name="jobs.edit"),
    path("<int:pk>/recommendations/", views.job_recommendations, name="jobs.recommendations"),
    path("<int:pk>/recommendations/debug/", views.job_recommendations_debug, name="jobs.recommendations_debug"),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('status/<int:job_id>/', views.application_status, name='application_status'),
    path('application/<int:application_id>/update_status/', views.update_status, name='update_status'),
    path('job/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('application/<int:application_id>/update_status/', views.update_status, name='update_status'),





]
