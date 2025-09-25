from django.db import models
from django.contrib.auth.models import User
from django.db import models

class JobSeeker(models.Model):
    id = models.AutoField(primary_key=True) # system user ID
    
    # general personal information
    firstName = models.CharField("First Name", max_length=255)
    lastName = models.CharField("Last Name", max_length=255)
    location = models.CharField("Location", max_length=255)
    image = models.ImageField("Profile Image", upload_to='jobSeeker_images/', null=True, blank=True)

    # education
    education = models.ForeignKey(
        "Institution",
        on_delete=models.PROTECT,
        related_name="jobSeeker") # one education per user
    degree = models.CharField(max_length=255)
    startYear = models.IntegerField("Start Year")
    endYear = models.IntegerField("End Year", blank=True)

    # professional
    headline = models.TextField()
    experience = models.ManyToManyField(
        "Experience",
        related_name="jobSeeker") # one education per user
    skills = models.ManyToManyField(
        "Skill",
        related_name="jobSeeker")

    def __str__(self):
        return str(self.id) + ' - ' + self.firstName + ' ' + self.lastName
    
class Institution(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    name = models.CharField(max_length=255) # name of the institution
    location = models.CharField(max_length=255) # location of the institution
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Experience(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    name = models.CharField("Company", max_length=255) # name of company
    location = models.CharField(max_length=255) # location worked
    startDate = models.CharField("Start Date (mm/yyyy)", max_length=7) # start date
    endDate = models.CharField("End Date (mm/yyyy)", max_length=7, blank=True) # end date
    description = models.TextField()
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Skill(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    skill = models.CharField(max_length=255)

    def job_seekers(self):
        return JobSeeker.objects.filter(skills=self)
    def __str__(self):
         return self.skill

class Link(models.Model):
    id = models.AutoField(primary_key=True) # system ID
    url = models.URLField() # link to be displayed
    jobSeeker = models.ForeignKey("JobSeeker", on_delete=models.CASCADE) # one user per link
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