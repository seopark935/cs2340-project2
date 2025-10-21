from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import recruiter_required
from django.contrib import messages
from .models import Job, Application
from .models import Job
from .forms import JobForm
from .filters import JobFilter
import requests
import json 
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# List jobs (everyone can see)
def job_list(request):
    qs = Job.objects.all().select_related("created_by").prefetch_related("skills")
    f = JobFilter(request.GET, queryset=qs)
    selected_remote_types = request.GET.getlist("remote_type")
    applied_jobs = []
    if request.user.is_authenticated:
        applied_jobs = Application.objects.filter(user=request.user).values_list('job_id', flat=True)

    applied_jobs = json.dumps(list(applied_jobs))


    location = request.GET.get("location")
    lat, lon = None, None

    if location:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"format": "json", "q": location},
            headers={"User-Agent": "job-finder/1.0"}
        )
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
    
    jobs_with_coords = []
    for job in f.qs:
        if job.address:
            try:
                response = requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"format": "json", "q": job.address},
                    headers={"User-Agent": "job-finder/1.0"}
                )
                data = response.json()
                if data:
                    job.lat = float(data[0]["lat"])
                    job.lng = float(data[0]["lon"])
                    jobs_with_coords.append(job)
            except Exception:
                continue

    jobs_json = json.dumps([
        {"title": job.title,
        "location": job.location,
        "remote_type": job.get_remote_type_display(),
        "visa": job.visa_sponsorship,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "skills": [s.name for s in job.skills.all()],
        "description": job.description,
        "id": job.id,
        "lat": job.lat,
        "lng": job.lng,
        }

        for job in jobs_with_coords 
            if job.lat is not None and job.lng is not None
    ])

    return render(request, "jobs/list.html", {
        "filter": f,
        "jobs": f.qs,
        "lat": lat,             
        "lon": lon,
        "jobs_json": jobs_json,
        "selected_remote_types": selected_remote_types,
        "applied_jobs": applied_jobs,
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


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        message = request.POST.get("message")
        Application.objects.create(job=job, user=request.user, message=message)
        messages.success(request, "Your application has been sent!")
        return redirect("jobs.list")
    return redirect("job_list")

@require_GET
def reverse_geocode(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': 'Missing lat or lon'}, status=400)

    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {'format': 'json', 'lat': lat, 'lon': lon}
    headers = {'User-Agent': 'MyCS2340Project/1.0 (yourname@example.com)'}  # valid User-Agent

    try:
        r = requests.get(url, params=params, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()
        return JsonResponse({'display_name': data.get('display_name', 'Unknown location')})
    except requests.RequestException:
        return JsonResponse({'display_name': 'Unknown location'})
    
@require_GET
def forward_geocode(request):
    address = request.GET.get('q')
    if not address:
        return JsonResponse({'error': 'Missing address'}, status=400)

    url = 'https://nominatim.openstreetmap.org/search'
    params = {'format': 'json', 'q': address}
    headers = {'User-Agent': 'MyCS2340Project/1.0 (yourname@example.com)'}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data:
            return JsonResponse({'lat': data[0]['lat'], 'lon': data[0]['lon']})
        return JsonResponse({'error': 'Address not found'}, status=404)
    except requests.RequestException:
        return JsonResponse({'error': 'Request failed'}, status=500)