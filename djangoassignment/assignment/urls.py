from django.urls import path, include
from assignment import views

urlpatterns = [
    path("", views.login_user, name="login"),
    path('dashboard/logout/', views.logout_user, name='logout'),
    path('dashboard/home/', views.home, name="home_page"),
    path('dashboard/movies/', views.get_movie_list_page, name="movie_list_page"),
    path('dashboard/users/', views.get_user_list_page, name="user_list_page"),
    path('dashboard/ratings/', views.get_movie_rating_list_page, name="rating_list_page"),
    path('dashboard/movie-rating-graph/', views.movie_rating_graph_page, name="rating_graph_page"),
]