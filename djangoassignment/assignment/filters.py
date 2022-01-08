from assignment.models import User, Rating
import django_filters


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = [
            'phone', 'user_id'
        ]


class MovieRatingFilter(django_filters.FilterSet):
    class Meta:
        model = Rating
        fields = [
            'movie', 'user', 'stars'
        ]

