# jobSeekers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import recruiter_required, jobseeker_required
from .models import JobSeeker
from .forms import JobSeekerForm


from django.db.models import Q

@login_required
@recruiter_required
def index(request):
    """List all job seekers (for recruiters only)."""
    name_term = request.GET.get("name", "")
    location_term = request.GET.get("location", "")
    skill_term = request.GET.get("skill", "")
    experience_term = request.GET.get("experience", "")


    # Start with all job seekers
    jobSeekers = JobSeeker.objects.filter(hide_profile=False)

    if name_term:
        jobSeekers = jobSeekers.filter(
            Q(firstName__icontains=name_term) |
            Q(lastName__icontains=name_term) |
            Q(headline__icontains=name_term)
        )

    if location_term:
        jobSeekers = jobSeekers.filter(location__icontains=location_term)

    if skill_term:
        jobSeekers = jobSeekers.filter(skills__icontains=skill_term)

    if experience_term:
        jobSeekers = jobSeekers.filter(experience__icontains=experience_term)

    # prevent duplicates when joining skills/projects
    jobSeekers = jobSeekers.distinct()

    template_data = {
        "title": "Job Seekers",
        "jobSeekers": jobSeekers,
    }
    return render(request, "jobSeekers/index.html", {"template_data": template_data})



@login_required
@recruiter_required
def show(request, id):
    """Show details of a single job seeker (for recruiters only)."""
    jobSeeker = get_object_or_404(JobSeeker, id=id)

    template_data = {
        "jobSeeker": jobSeeker,
        "name": f"{jobSeeker.firstName} {jobSeeker.lastName}",
        "experiences": jobSeeker.experience.all(),  # ManyToMany forward relation
        "skills": jobSeeker.skills.all(),
        "links": jobSeeker.links.all(),
        "hide_profile": jobSeeker.hide_profile,
    }

    return render(request, "jobSeekers/show.html", {"template_data": template_data})


@login_required
@jobseeker_required
def my_profile(request):
    """Allow a job seeker to view their own profile."""
    jobSeeker = get_object_or_404(JobSeeker, user=request.user)  # ✅ safe forward lookup

    template_data = {
        "jobSeeker": jobSeeker,
        "name": f"{jobSeeker.firstName} {jobSeeker.lastName}",
        "experiences": jobSeeker.experience.all(),
        "skills": jobSeeker.skills.all(),
        "links": jobSeeker.links.all(),
    }
    return render(request, "jobSeekers/show.html", {"template_data": template_data})


@login_required
@jobseeker_required
def edit_profile(request):
    """Allow a job seeker to edit their own profile."""
    jobSeeker = get_object_or_404(JobSeeker, user=request.user)  # ✅ safe forward lookup

    if request.method == "POST":
        form = JobSeekerForm(request.POST, request.FILES, instance=jobSeeker)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("jobSeekers.my_profile")
    else:
        form = JobSeekerForm(instance=jobSeeker)

    return render(request, "jobSeekers/edit.html", {"form": form})
