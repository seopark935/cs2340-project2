# jobSeekers/models.py
from django.db import models
from django.conf import settings  # use settings.AUTH_USER_MODEL

class JobSeeker(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobseeker_profile"
    )

    # general personal information
    firstName = models.CharField("First Name", max_length=255)
    lastName  = models.CharField("Last Name", max_length=255)
    location  = models.CharField("Location", max_length=255, blank=True)
    image     = models.ImageField("Profile Image", upload_to='jobSeeker_images/', null=True, blank=True)

    # education
    education = models.ForeignKey("Institution", on_delete=models.PROTECT, related_name="jobSeekers", null=True, blank=True)
    degree    = models.CharField(max_length=255, blank=True)
    startYear = models.IntegerField("Start Year", null=True, blank=True)
    endYear   = models.IntegerField("End Year", null=True, blank=True)

    # professional
    headline   = models.TextField(blank=True)
    experience = models.ManyToManyField("Experience", related_name="jobSeekers", blank=True)
    skills     = models.ManyToManyField("Skill", related_name="jobSeekers", blank=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    @property
    def full_name(self):
        return f"{self.firstName} {self.lastName}"


class Institution(models.Model):
    name     = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    def __str__(self): return self.name


class Experience(models.Model):
    name        = models.CharField("Company", max_length=255)
    location    = models.CharField(max_length=255, blank=True)
    startDate   = models.CharField("Start Date (mm/yyyy)", max_length=7)
    endDate     = models.CharField("End Date (mm/yyyy)", max_length=7, blank=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name


class Skill(models.Model):
    # your admin used `name` earlier; standardize on `name`
    name = models.CharField(max_length=255, unique=True)
    def __str__(self): return self.name


class Link(models.Model):
    url        = models.URLField()
    jobSeeker  = models.ForeignKey("JobSeeker", on_delete=models.CASCADE, related_name="links")
    def __str__(self): return self.url



# class Movie(models.Model): # controls model properties
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     price = models.IntegerField()
#     description = models.TextField()
#     image = models.ImageField(upload_to='movie_images/')
#     amount_left = models.PositiveIntegerField(default=1) #new
#     def __str__(self):
#         return str(self.id) + ' - ' + self.name

# class Review(models.Model):
#     id = models.AutoField(primary_key=True)
#     comment = models.CharField(max_length=255)
#     date = models.DateTimeField(auto_now_add=True)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     likes = models.PositiveIntegerField(default=0) # new
#     def __str__(self):
#         return str(self.id) + ' - ' + self.movie.name