from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import recruiter_required, jobseeker_required
from django.contrib import messages
from .models import Job, Application
from .models import Job
from .forms import JobForm
from .filters import JobFilter

# List jobs (everyone can see)
def job_list(request):
    qs = Job.objects.all().select_related("created_by").prefetch_related("skills")
    f = JobFilter(request.GET, queryset=qs)
    selected_remote_types = request.GET.getlist("remote_type")
    applied_jobs = []
    if request.user.is_authenticated and request.user.is_jobseeker:
        applied_jobs = Application.objects.filter(user=request.user).values_list('job_id', flat=True)
    return render(request, "jobs/list.html", {
        "filter": f,
        "jobs": f.qs,
        "selected_remote_types": selected_remote_types,
        "applied_jobs": applied_jobs,
    })

# Recruiter dashboard (see own jobs only)
@login_required
@recruiter_required
def job_dashboard(request):
    if request.user.is_recruiter:
        jobs = Job.objects.filter(created_by=request.user)
        applications = Application.objects.filter(job__in=jobs)
        return render(request, 'jobs/dashboard.html', {'jobs': jobs, 'applications': applications})
    else:
        return redirect('jobs.list')
  

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

#Apply Job 
@login_required
@jobseeker_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    existing = Application.objects.filter(job=job, user=request.user).exists()
    if existing:
        messages.info(request, "You’ve already applied for this job.")
        return redirect("jobs.list")
    # Only process POST requests
    if request.method == "POST":
        message = request.POST.get("message")

        # Create the application with default Applied status
        Application.objects.create(
            job=job,
            user=request.user,
            message=message,
            status=Application.Status.APPLIED  # <- new
        )

        messages.success(request, "Your application has been sent!")
        return redirect("jobs.list")

    # Redirect GET requests back to job list
    return redirect("jobs.list")

#Status window
@login_required
def application_status(request, job_id):
    # Only allow job seekers
    if not request.user.is_jobseeker:
        return redirect('jobs.list')

    # Get the application for this job by this user
    application = get_object_or_404(
        Application,
        job_id=job_id,
        user=request.user
    )

    return render(request, 'jobs/application_status.html', {
        'application': application
    })

#Review Application
@login_required
@recruiter_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, created_by=request.user)
    applications = Application.objects.filter(job=job)

    # Group applications by status
    kanban_columns = {status: [] for status, _ in Application.Status.choices}
    for app in applications:
        kanban_columns[app.status].append(app)

    return render(request, 'jobs/job_application_kanban.html', {
        'job': job,
        'kanban_columns': kanban_columns,
        'status_choices': Application.Status.choices,  # list of (value, label)
    })

@login_required
@recruiter_required
def update_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Application.Status.choices).keys():
            application.status = new_status
            application.save()
            messages.success(request, f"Status updated to {application.get_status_display()}.")
        else:
            messages.error(request, "Invalid status selected.")
        return redirect('job_applications', job_id=application.job.id)
