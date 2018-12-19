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


class InitialReviewAdmin(admin.ModelAdmin):
    fields = ['movie', 'review_text', 'watch_for', 'rating', 'reviewer', 'pub_date']
    search_fields = ['review_text', 'watch_for']
    list_display = ('reviewer', 'pub_date', 'movie', 'rating', 'review_text', 'watch_for')
    list_filter = ['pub_date', 'rating', 'reviewer', 'movie']


class RewatchReviewAdmin(admin.ModelAdmin):
    fields = ['movie', 'review_text', 'discovery', 'rating', 'reviewer', 'pub_date']
    search_fields = ['review_text', 'discovery']
    list_display = ('reviewer', 'pub_date', 'movie', 'rating', 'review_text', 'discovery')
    list_filter = ['pub_date', 'rating', 'reviewer', 'movie']


admin.site.register(Movie, MovieAdmin)
admin.site.register(InitialReview, InitialReviewAdmin)
admin.site.register(RewatchReview, RewatchReviewAdmin)
admin.AdminSite.site_header = "Review Site Administration"
