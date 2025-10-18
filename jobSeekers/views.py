# jobSeekers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.decorators import recruiter_required, jobseeker_required
from .models import JobSeeker, Skill, Experience, Link
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


    # Base querySet (public profiles only)
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
        jobSeekers = jobSeekers.filter(skills__name__icontains=skill_term)

    if experience_term:
        jobSeekers = jobSeekers.filter(experience__name__icontains=experience_term)

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
    
    template_data = {}
    template_data['form'] = form
    template_data['jobSeeker'] = jobSeeker

    return render(request, "jobSeekers/edit.html", {"template_data": template_data})

@login_required
@jobseeker_required
def add_skill(request):
    jobSeeker = get_object_or_404(JobSeeker, user=request.user)

    name = (request.POST.get("name") or "").strip()
    if not name:
        return HttpResponseBadRequest("Skill name required.")

    skill = Skill()
    skill.name = name
    skill.save()
    jobSeeker.skills.add(skill)
    jobSeeker.save()

    # redirect back to your editor page (adjust the URL name/args to your project)
    return redirect("jobSeekers.edit_profile")

@login_required
@jobseeker_required
def add_link(request):
    jobSeeker = get_object_or_404(JobSeeker, user=request.user)

    name = (request.POST.get("name") or "").strip()
    if not name:
        return HttpResponseBadRequest("Skill name required.")

    link = Link()
    link.url = name
    link.save()
    jobSeeker.links.add(link)
    jobSeeker.save()

    # redirect back to your editor page (adjust the URL name/args to your project)
    return redirect("jobSeekers.edit_profile")

@login_required
@jobseeker_required
def add_experience(request):
    jobSeeker = get_object_or_404(JobSeeker, user=request.user)

    name = (request.POST.get("name") or "").strip()
    location = (request.POST.get("location") or "").strip()
    startDate = (request.POST.get("startDate") or "").strip()
    endDate = (request.POST.get("endDate") or "").strip()
    description = (request.POST.get("description") or "").strip()

    experience = Experience()
    experience.name = name
    experience.location = location
    experience.startDate = startDate
    experience.endDate = endDate
    experience.description = description
    experience.save()
    jobSeeker.experience.add(experience)
    jobSeeker.save()

    # redirect back to your editor page (adjust the URL name/args to your project)
    return redirect("jobSeekers.edit_profile")