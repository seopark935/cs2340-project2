from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='jobSeekers.index'),
    path('<int:id>/', views.show, name='jobSeekers.show'),
    path("me/", views.my_profile, name="jobSeekers.my_profile"), 
    path("me/edit/", views.edit_profile, name="jobSeekers.edit_profile"),
    path("me/add_skill/", views.add_skill, name="jobSeekers.add_skill"),
    path("me/add_link/", views.add_link, name="jobSeekers.add_link"),
    path("me/add_experience/", views.add_experience, name="jobSeekers.add_experience"),
    path("me/save_search/", views.save_candidate_search, name="jobSeekers.save_candidate_search"),
    path("<int:id>/apply_search/", views.apply_candidate_search, name="jobSeekers.apply_candidate_search"),
    path("<int:id>/delete_search/", views.delete_candidate_search, name="jobSeekers.delete_candidate_search"),
    path("me/refresh_search/", views.refresh_candidate_searches, name="jobSeekers.refresh_candidate_searches"),
]