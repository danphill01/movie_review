from django.contrib import admin

from .models import Movie, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 2


class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['title', 'plot']}), 
        ('Details', {'fields': ['runtime', 'rated', 'year', 'imdb_id']}), 
    ]
    inlines = [ReviewInline]
    list_display = ('title', 'year', 'rated')
    list_filter = ['year', 'rated']
    search_fields = ['title', 'plot']

admin.site.register(Movie, MovieAdmin)
admin.AdminSite.site_header = "Review Site Administration"
