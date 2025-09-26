# jobSeekers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import recruiter_required, jobseeker_required
from .models import JobSeeker
from .forms import JobSeekerForm


@login_required
@recruiter_required
def index(request):
    """List all job seekers (for recruiters only)."""
    search_term = request.GET.get("search", "")

    # Start with all job seekers
    """jobSeekers = JobSeeker.objects.all()"""
    jobSeekers = JobSeeker.objects.filter(hide_profile=False)

    # Apply search if provided
    if search_term:
        jobSeekers = jobSeekers.filter(
            Q(firstName__icontains=search_term) |
            Q(lastName__icontains=search_term) |
            Q(headline__icontains=search_term)
        )

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
        "experiences": jobSeeker.experience.all(),   # ManyToMany forward relation
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
