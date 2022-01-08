from django.contrib import admin
from assignment.models import Movie, User, Rating


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('user_id', 'first_name', 'last_name', 'phone')


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ('title', 'description')


class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('movie', 'user', 'stars')
    list_filter = ('movie', 'user')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'movie', 'user',
        )


admin.site.register(User, UserAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)