# jobSeekers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.decorators import recruiter_required, jobseeker_required
from .models import JobSeeker, Skill, Experience, Link, CandidateSearch
from .forms import JobSeekerForm
from django.db.models import Q, Count
from django.urls import reverse
from urllib.parse import urlencode
from jobs.models import Job, Application

def build_jobseeker_qs(name="", location="", skill="", experience=""):
    qs = JobSeeker.objects.filter(hide_profile=False)
    if name:
        qs = qs.filter(
            Q(firstName__icontains=name) |
            Q(lastName__icontains=name) |
            Q(headline__icontains=name)
        )
    if location:
        qs = qs.filter(location__icontains=location)
    if skill:
        qs = qs.filter(skills__name__icontains=skill)
    if experience:
        qs = qs.filter(experience__name__icontains=experience)
    return qs.distinct()

def _norm(s):
    # normalize: None -> "", strip spaces, lowercase
    return (s or "").strip().lower()

@login_required
@recruiter_required
def index(request):
    """List all job seekers (for recruiters only)."""
    name_term = request.GET.get("name", "")
    location_term = request.GET.get("location", "")
    skill_term = request.GET.get("skill", "")
    experience_term = request.GET.get("experience", "")


    # Base querySet (public profiles only)
    jobSeekers = build_jobseeker_qs(name_term, location_term, skill_term, experience_term)

    candidateSearches = (
        CandidateSearch.objects
        .filter(user=request.user)
        .annotate(matches_count=Count("matches", distinct=True))
        .prefetch_related("matches")  # optional if you also list them
    )

    # attach a flag to each search indicating if it matches the current filters
    for cs in candidateSearches:
        cs.is_current = (
            _norm(cs.nameHeadline) == name_term and
            _norm(cs.location)     == location_term and
            _norm(cs.skill)        == skill_term and
            _norm(cs.experience)   == experience_term
        )

    template_data = {
        "title": "Job Seekers",
        "jobSeekers": jobSeekers,
        "candidateSearches": candidateSearches,
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

    job_seeker_skills = jobSeeker.skills.all()
    applied_jobs = Application.objects.filter(user=request.user).values_list('job_id', flat=True)

    recommended_jobs = (
        Job.objects
        .filter(skills__in=job_seeker_skills)
        .exclude(id__in=applied_jobs)
        .annotate(matching_skills=Count('skills'))
        .order_by('-matching_skills', '-created_at')
        .distinct()[:5]
    )

    template_data = {
        "jobSeeker": jobSeeker,
        "name": f"{jobSeeker.firstName} {jobSeeker.lastName}",
        "experiences": jobSeeker.experience.all(),
        "skills": jobSeeker.skills.all(),
        "links": jobSeeker.links.all(),
        "recommended_jobs": recommended_jobs,
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

@login_required
@recruiter_required
def save_candidate_search(request):
    name_term = request.GET.get("name", "")
    location_term = request.GET.get("location", "")
    skill_term = request.GET.get("skill", "")
    experience_term = request.GET.get("experience", "")

    if (name_term == "" and location_term == "" and skill_term == "" and experience_term == ""):
        return redirect("jobSeekers.index")

    # case-insensitive duplicate check for this user
    existing = (
        CandidateSearch.objects
        .filter(user=request.user)
        .filter(
            Q(nameHeadline__iexact=name_term) &
            Q(location__iexact=location_term) &
            Q(skill__iexact=skill_term) &
            Q(experience__iexact=experience_term)
        )
        .first()
    )

    if (existing):
        messages.error(request, "This search is already saved.")
        return redirect("jobSeekers.index")

    candidateSearch = CandidateSearch.objects.create(
        user=request.user,
        nameHeadline=name_term,
        location=location_term,
        skill=skill_term,
        experience=experience_term,
    )
    candidateSearch.matches.set(build_jobseeker_qs(name_term, location_term, skill_term, experience_term))

    candidateSearch.save()

    params = {
        "name": candidateSearch.nameHeadline or "",
        "location": candidateSearch.location or "",
        "skill": candidateSearch.skill or "",
        "experience": candidateSearch.experience or "",
    }

    url = reverse("jobSeekers.index") + "?" + urlencode(params)
    return redirect(url)

@login_required
@recruiter_required
def apply_candidate_search(request, id):
    candidateSearch = get_object_or_404(CandidateSearch, id=id)

    params = {
        "name": candidateSearch.nameHeadline or "",
        "location": candidateSearch.location or "",
        "skill": candidateSearch.skill or "",
        "experience": candidateSearch.experience or "",
    }

    url = reverse("jobSeekers.index") + "?" + urlencode(params)
    return redirect(url)

@login_required
@recruiter_required
def delete_candidate_search(request, id):
    candidateSearch = get_object_or_404(CandidateSearch, id=id)
    candidateSearch.delete()

    return redirect("jobSeekers.index")

@login_required
@recruiter_required
def refresh_candidate_searches(request):
    candidateSearches = CandidateSearch.objects.filter(user=request.user)
    for cs in candidateSearches:
        prev_matches = cs.matches.count()

        name_term = cs.nameHeadline
        location_term = cs.location
        skill_term = cs.skill
        experience_term = cs.experience

        # Base querySet (public profiles only)
        jobSeekers = build_jobseeker_qs(name_term, location_term, skill_term, experience_term)

        cs.matches.set(jobSeekers)

        curr_matches = cs.matches.count()
        if (curr_matches > prev_matches):
            messages.success(request, f"{curr_matches - prev_matches} New Matches!") # notify new matches

    return redirect("jobSeekers.index")