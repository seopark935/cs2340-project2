# jobSeekers/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.decorators import recruiter_required
from .models import JobSeeker

@login_required
@recruiter_required
def index(request):
    """List all job seekers (for recruiters only)."""
    search_term = request.GET.get("search", "")

    # Start with all job seekers
    jobSeekers = JobSeeker.objects.all()

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
        "name": jobSeeker.full_name,
        "experiences": jobSeeker.experience.all(),   # ✅ correct ManyToMany usage
        "skills": jobSeeker.skills.all(),            # ✅ correct ManyToMany usage
        "links": jobSeeker.links.all(),              # ✅ via related_name="links"
    }

    return render(request, "jobSeekers/show.html", {"template_data": template_data})


    # movie = Movie.objects.get(id=id)
    # reviews = Review.objects.filter(movie=movie)
    # template_data = {}
    # template_data['title'] = movie.name
    # template_data['movie'] = movie
    # template_data['reviews'] = reviews
    # return render(request, 'movies/show.html',
    #               {'template_data': template_data}

# @login_required
# def create_review(request, id):
#     if request.method == 'POST' and request.POST['comment'] != '':
#         movie = Movie.objects.get(id=id)
#         print("here\n")
#         review = Review()
#         print("created\n")
#         review.comment = request.POST['comment']
#         review.movie = movie
#         review.user = request.user
#         review.save()
#         return redirect('movies.show', id=id)
#     else:
#         return redirect('movies.show', id=id)
    
# @login_required
# def edit_review(request, id, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     if request.user != review.user:
#         return redirect('movies.show', id=id)
#     if request.method == 'GET':
#         template_data = {}
#         template_data['title'] = 'Edit Review'
#         template_data['review'] = review
#         return render(request, 'movies/edit_review.html', {'template_data': template_data})
#     elif request.method == 'POST' and request.POST['comment'] != '':
#         review = Review.objects.get(id=review_id)
#         review.comment = request.POST['comment']
#         review.save()
#         return redirect('movies.show', id=id)
#     else:
#         return redirect('movies.show', id=id)
    

# @login_required
# def delete_review(request, id, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     review.delete()
#     return redirect('movies.show', id=id)

# def like_review(request, id, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     review.likes += 1
#     review.save()
#     return redirect('movies.show', id=id)

# def sort_review(request, id):
#     movie = Movie.objects.get(id=id)
#     reviews = Review.objects.filter(movie=movie).order_by('-likes')
#     template_data = {}
#     template_data['title'] = movie.name
#     template_data['movie'] = movie
#     template_data['reviews'] = reviews
#     return render(request, 'movies/show.html',
#                   {'template_data': template_data})

