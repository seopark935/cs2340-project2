# jobSeekers/models.py
from django.db import models
from django.conf import settings  # use settings.AUTH_USER_MODEL
from django.urls import reverse

class Skill(models.Model):
    # your admin used `name` earlier; standardize on `name`
    name = models.CharField(max_length=255, unique=True)
    def __str__(self): return self.name

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
    education = models.ForeignKey("Institution", on_delete=models.PROTECT, related_name="jobSeeker", null=True, blank=True)
    degree    = models.CharField(max_length=255, blank=True)
    startYear = models.IntegerField("Start Year", null=True, blank=True)
    endYear   = models.IntegerField("End Year", null=True, blank=True)

    # professional
    headline   = models.TextField(blank=True)
    experience = models.ManyToManyField("Experience", related_name="jobSeeker", blank=True)
    skills     = models.ManyToManyField("Skill", related_name="jobSeeker", blank=True)
    links      = models.ManyToManyField("Link", related_name="jobSeeker", blank=True)

    #privacy
    hide_image = models.BooleanField(default=False)
    hide_headline = models.BooleanField(default=False)
    hide_profile = models.BooleanField(default=False)
    hide_location = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("jobSeekers.show", args=[self.id])
    
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

class Link(models.Model):
    url        = models.URLField()
    def __str__(self): return self.url

class CandidateSearch(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,           # maps to the recruiter’s user
        on_delete=models.CASCADE,
        related_name="candidate_searches",
    )
    nameHeadline = models.CharField("Name or Headline", max_length=255)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255)
    skill = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)

    matches = models.ManyToManyField(JobSeeker, related_name="matched_searches", blank=True)

    def __str__(self): return str(self.id)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="notifications")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["user", "-created_at"])]