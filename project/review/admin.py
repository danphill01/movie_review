from django.contrib import admin

from .models import Movie, InitialReview, RewatchReview


class InitialReviewInline(admin.TabularInline):
    model = InitialReview
    extra = 1


class RewatchReviewInline(admin.TabularInline):
    model = RewatchReview
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['title', 'plot']}), 
        ('Details', {'fields': ['runtime', 'rated', 'year', 'imdb_id']}), 
    ]
    inlines = [InitialReviewInline, RewatchReviewInline]
    list_display = ('title', 'year', 'rated')
    list_filter = ['year', 'rated']
    search_fields = ['title', 'plot']

admin.site.register(Movie, MovieAdmin)
admin.site.register(InitialReview)
admin.site.register(RewatchReview)
admin.AdminSite.site_header = "Review Site Administration"
