from django.contrib import admin
from .models import Movie

# Register your models here.
class Admin_movie(admin.ModelAdmin):
    list_display = ('title', 'overview', 'poster_path')

admin.site.register(Movie, Admin_movie)