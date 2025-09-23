from django.contrib import admin
from .models import JobSeekerProfile, Institution, Skill, Link

class JobSeekerProfileAdmin(admin.ModelAdmin):
    search_fields = ['firstName']
    autocomplete_fields = ('education',)
    filter_horizontal = ("skills",)  # editable list of skills

class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ("name", "location")   # needed for autocomplete

class SkillAdmin(admin.ModelAdmin):
    search_fields = ['name']

    # def profiles_count(self, obj):
    #     return obj.job_seekers.count()

    # def job_seekers_list(self, obj):
    #     names = obj.job_seekers.values_list("firstName", "lastName")
    #     return ", ".join(f"{fn} {ln}" for fn, ln in names)

class LinkAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
admin.site.register(Institution, InstitutionAdmin)
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