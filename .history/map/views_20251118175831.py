from django.shortcuts import render
from jobs.models import Job, Application
import requests
import json
import math


def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(math.radians(lon2 - lon1)/2)**2)
    return 2 * R * math.asin(math.sqrt(a))


def geocode(address):
    try:
        res = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"format": "json", "q": address},
            headers={"User-Agent": "job-finder/1.0"}
        ).json()
        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])
    except:
        pass
    return None, None


def index(request):
    radius_enabled = request.GET.get("radius", "on") == "on"

    user_lat = None
    user_lng = None
    radius = None

    if request.user.is_authenticated and getattr(request.user, 'is_jobseeker', False):
        radius = request.user.jobseeker_profile.preferred_radius_miles

        home = request.user.jobseeker_profile.location
        if home:
            user_lat, user_lng = geocode(home)

    qs = Job.objects.all().prefetch_related("skills")
    jobs_with_coords = []

    for job in qs:
        if not job.address:
            continue

        lat, lng = geocode(job.address)
        if lat is None or lng is None:
            continue

        job.lat = lat
        job.lng = lng

        if radius_enabled and user_lat and user_lng and radius:
            distance = haversine(user_lat, user_lng, lat, lng)
            if distance <= radius:
                jobs_with_coords.append(job)
        else:
            jobs_with_coords.append(job)

    jobs_json = json.dumps([
        {
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "remote_type": job.get_remote_type_display(),
            "visa": job.visa_sponsorship,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "skills": [s.name for s in job.skills.all()],
            "description": job.description,
            "lat": job.lat,
            "lng": job.lng,
        }
        for job in jobs_with_coords
    ])

    applied_ids = []
    if request.user.is_authenticated and getattr(request.user, 'is_jobseeker', False):
        applied_ids = list(
            Application.objects.filter(user=request.user)
            .values_list('job_id', flat=True)
        )

    return render(request, "map/index.html", {
        "jobs_json": jobs_json,
        "applied_ids": json.dumps(applied_ids),
        "user_radius": radius,
        "radius_enabled": radius_enabled,
        "user_lat": user_lat,
        "user_lng": user_lng,
        "user_is_authenticated": request.user.is_authenticated,
        "user_is_jobseeker": getattr(request.user, 'is_jobseeker', False),
    })
