from django.contrib import admin
from .models import JobSeeker, Institution, Experience, Skill, Link

class JobSeekerAdmin(admin.ModelAdmin):
    search_fields = ['firstName', 'lastName', 'headline']
    autocomplete_fields = ('education',)
    filter_horizontal = ("skills", "experience")  # many-to-many pickers

class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ("name", "location")   # needed for autocomplete

class ExperienceAdmin(admin.ModelAdmin):
    search_fields = ("name", "location")   # needed for autocomplete

class SkillAdmin(admin.ModelAdmin):
    search_fields = ['name']

class LinkAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Link, LinkAdmin)


# class MovieAdmin(admin.ModelAdmin): # controls how it looks and behaves
#     ordering = ['name']
#     search_fields = ['name']
#     def get_readonly_fields(self, request, obj=None):
#         ro = list(super().get_readonly_fields(request, obj))
#         if obj and obj.amount_left <= 0:
#             ro.append("amount_left")
#         return ro
# admin.site.register(Movie, MovieAdmin)
# admin.site.register(Review)