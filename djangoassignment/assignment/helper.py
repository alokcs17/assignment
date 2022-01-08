from assignment.models import Movie, User


def get_movie_listing_serialized_data(movies):
    movie_json = movies.values('id', 'title', 'description')

    return list(movie_json)


def get_user_listing_serialized_data(users):
    user_json = users.values('id', 'first_name', 'last_name', 'user_id', 'phone', 'email')

    for each_user in user_json:
        each_user['user_name'] = each_user['first_name'] + " " + each_user['last_name']

    return list(user_json)


def get_movie_rating_listing_serialized_data(ratings):
    ratings_json = ratings.values('id', 'movie_id', 'user_id', 'stars')

    movie_dict = dict(Movie.objects.values_list('id', 'title').all())
    user_first_name_dict = dict(User.objects.values_list('id', 'first_name').all())
    user_last_name_dict = dict(User.objects.values_list('id', 'last_name').all())

    for each_rating in ratings_json:
        each_rating['movie_name'] = movie_dict.get(each_rating['movie_id'], '--')
        each_rating['user_name'] = user_first_name_dict.get(each_rating['user_id'], '--') + " " + \
                                   user_last_name_dict.get(each_rating['user_id'], '--')

    return list(ratings_json)

