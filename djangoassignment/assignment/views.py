import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from assignment.decorators import dashboard_admin_request, validate_permissions
from assignment.helper import get_movie_listing_serialized_data, get_user_listing_serialized_data, get_movie_rating_listing_serialized_data
from assignment.models import Movie, Rating, User
from assignment.filters import UserFilter, MovieRatingFilter


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('home/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    with transaction.atomic():
                        login(request, user)
                        return HttpResponseRedirect('home/')
                return HttpResponse('Account is not active at the moment. Please contact admin.')
            else:
                messages.info(request, 'Username or Password is Incorrect')
        return render(request, 'assignment/login.html', {})


@validate_permissions(login_required(login_url='login'), dashboard_admin_request)
def home(request):
    context = {}
    return render(request, 'assignment/index.html', context)


@validate_permissions(login_required(login_url='login'), dashboard_admin_request)
def get_movie_list_page(request):
    movies = Movie.objects.all()
    context = {
        'movies': get_movie_listing_serialized_data(movies)
    }
    return render(request, 'assignment/movie_list_page.html', context)


@validate_permissions(login_required(login_url='login'), dashboard_admin_request)
def get_user_list_page(request):
    users = User.objects.all()
    my_filter = UserFilter(request.GET, users)
    context = {
        'myFilter': my_filter,
        'users': get_user_listing_serialized_data(my_filter.qs)
    }
    return render(request, 'assignment/get_user_listing_page.html', context)


@validate_permissions(login_required(login_url='login'), dashboard_admin_request)
def get_movie_rating_list_page(request):
    ratings = Rating.objects.all()
    my_filter = MovieRatingFilter(request.GET, ratings)
    context = {
        'myFilter': my_filter,
        'ratings': get_movie_rating_listing_serialized_data(my_filter.qs)
    }
    return render(request, 'assignment/get_movie_rating_listing_page.html', context)


@validate_permissions(login_required(login_url='login'), dashboard_admin_request)
def movie_rating_graph_page(request):
    movie_rating_user_data_source = {
        'name': "Movie Rating User Graph",
        "data": []
    }
    rating_entries = Rating.objects.values('movie__title').annotate(tot=Count('id'))
    for key in rating_entries:
        data = {
            'name': [key['movie__title']],
            'y': key['tot'],

        }
        movie_rating_user_data_source['data'].append(data)

    movie_rating_avg_data_source = {
        'name': "Average Movie Rating Graph",
        "data": []
    }
    movie_avg_rating_entries = Rating.objects.values('movie__title').annotate(avg_rating=Avg('stars'))
    for key in movie_avg_rating_entries:
        data = {
            'name': [key['movie__title']],
            'y': key['avg_rating'],

        }
        movie_rating_avg_data_source['data'].append(data)

    movie_rating_user_chart_data = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Total Movie User Ratings'},
        'accessibility': {
            'announceNewData': {
                'enabled': True
            }
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'y': -5,
                    'showInLegend': True,
                    'innerSize': '40%',
                    'connectorShape': 'fixedOffset',
                    'format': '{point.name}: <br>{point.percentage:.1f} %<br>total: {point.y}',
                    'padding': 0,
                    'style': {
                        'fontSize': '11px',
                        'fontFamily': 'tahoma',
                        'textShadow': False,
                        'useHTML': True,
                    }
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px; color:#8e5ea2">{series.name}<br>{point.percentage:.1f} %'
                            '</span><br>',
            'pointFormat': '<span style="color:#3cba9f">{point.name}</span>: <b>{point.y}</b><br/>'
        },
        'series': [movie_rating_user_data_source],

    }

    movie_rating_average_chart_data = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Movie Average Rating Data'},
        'accessibility': {
            'announceNewData': {
                'enabled': True
            }
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'y': -5,
                    'showInLegend': True,
                    'innerSize': '40%',
                    'connectorShape': 'fixedOffset',
                    'format': '{point.name}: <br>{point.percentage:.1f} %<br>total_average: {point.y}',
                    'padding': 0,
                    'style': {
                        'fontSize': '11px',
                        'fontFamily': 'tahoma',
                        'textShadow': False,
                        'useHTML': True,
                    }
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px; color:#8e5ea2">{series.name}<br>{point.percentage:.1f} %'
                            '</span><br>',
            'pointFormat': '<span style="color:#3cba9f">{point.name}</span>: <b>{point.y}</b><br/>'
        },
        'series': [movie_rating_avg_data_source],

    }

    context = {
        'movie_rating_data': json.dumps(movie_rating_user_chart_data),
        'movie_rating_avg_data': json.dumps(movie_rating_average_chart_data)
    }
    return render(request, 'assignment/get_movie_rating_graph_page.html', context)