from django.db import models
from django.contrib.auth.models import User
from django.db import models

class JobSeekerProfile(models.Model):
    id = models.AutoField(primary_key=True) # system user ID
    
    # general personal information
    firstName = models.CharField("First Name", max_length=255)
    lastName = models.CharField("Last Name", max_length=255)
    location = models.CharField("Location", max_length=255)
    profileImage = models.ImageField("Profile Image", upload_to='jobseeker_images/')

    # education
    education = models.ForeignKey(
        "Institution",
        on_delete=models.PROTECT,
        related_name="job_seekers") # one education per user
    degree = models.CharField(max_length=255)
    startYear = models.IntegerField("Start Year")
    endYear = models.IntegerField("End Year")

    # professional
    headline = models.TextField()
    skills = models.ManyToManyField(
        "Skill",
        related_name="job_seekers")

    def __str__(self):
        return str(self.id) + ' - ' + self.firstName + ' ' + self.lastName
    
class Institution(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    name = models.CharField(max_length=255) # name of the institution
    location = models.CharField(max_length=255) # location of the institution
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Skill(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    skill = models.CharField(max_length=255)

    def job_seekers(self):
        return JobSeekerProfile.objects.filter(skills=self)
    def __str__(self):
         return self.skill

class Link(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    url = models.URLField() # link to be displayed
    jobSeeker = models.ForeignKey("JobSeekerProfile", on_delete=models.CASCADE) # one user per link
    def __str__(self):
        return str(self.id) + ' - ' + self.url


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