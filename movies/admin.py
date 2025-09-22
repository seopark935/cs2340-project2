from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin): # controls how it looks and behaves
    ordering = ['name']
    search_fields = ['name']
    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if obj and obj.amount_left <= 0:
            ro.append("amount_left")
        return ro
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)