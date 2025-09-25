# jobs/models.py
from django.db import models
from django.conf import settings
from jobSeekers.models import Skill

class Job(models.Model):
    class RemoteType(models.TextChoices):
        ONSITE = "ONSITE", "On-site"
        REMOTE = "REMOTE", "Remote"
        HYBRID = "HYBRID", "Hybrid"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    title            = models.CharField(max_length=200, db_index=True)
    description      = models.TextField()
    location         = models.CharField(max_length=200, db_index=True)
    remote_type      = models.CharField(max_length=6, choices=RemoteType.choices, db_index=True)
    salary_min       = models.PositiveIntegerField(null=True, blank=True)
    salary_max       = models.PositiveIntegerField(null=True, blank=True)
    currency         = models.CharField(max_length=3, default="USD")
    visa_sponsorship = models.BooleanField(default=False, db_index=True)
    skills           = models.ManyToManyField(Skill, blank=True, related_name="jobs")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",
        limit_choices_to={"role": "RECRUITER"},
    )
    status     = models.CharField(max_length=6, choices=Status.choices, default=Status.OPEN, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["location"]),
            models.Index(fields=["remote_type"]),
            models.Index(fields=["visa_sponsorship"]),
        ]
