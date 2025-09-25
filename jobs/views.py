from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import recruiter_required
from .models import Job
from .forms import JobForm
from .filters import JobFilter

# List jobs (everyone can see)
def job_list(request):
    qs = Job.objects.all().select_related("created_by").prefetch_related("skills")
    f = JobFilter(request.GET, queryset=qs)
    selected_remote_types = request.GET.getlist("remote_type")
    return render(request, "jobs/list.html", {
        "filter": f,
        "jobs": f.qs,
        "selected_remote_types": selected_remote_types,
    })

# Recruiter dashboard (see own jobs only)
@login_required
@recruiter_required
def job_dashboard(request):
    jobs = Job.objects.filter(created_by=request.user)
    return render(request, "jobs/dashboard.html", {"jobs": jobs})

# Create new job
@login_required
@recruiter_required
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            form.save_m2m()
            return redirect("jobs.dashboard")
    else:
        form = JobForm()
    return render(request, "jobs/create.html", {"form": form})

# Edit job (only if recruiter owns it)
@login_required
@recruiter_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("jobs.dashboard")
    else:
        form = JobForm(instance=job)
    return render(request, "jobs/edit.html", {"form": form, "job": job})
