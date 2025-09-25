# jobs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import recruiter_required
from .models import Job
from .filters import JobFilter
from .forms import JobForm

def job_list(request):
    qs = Job.objects.filter(status=Job.Status.OPEN).select_related("created_by").prefetch_related("skills")
    f = JobFilter(request.GET, queryset=qs)
    return render(request, "jobs/list.html", {"filter": f, "jobs": f.qs})

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
            return redirect("jobs.list")
    else:
        form = JobForm()
    return render(request, "jobs/create.html", {"form": form})
