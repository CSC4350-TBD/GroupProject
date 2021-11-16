from moviedb import get_movie_info, get_id, get_movie_recs
from imdb import get_imdb_id
from model import saved_movies, ignored_movies
from flask_login import current_user
import secrets
from app import db


def get_recommendation(search_term):  # this is where you will pass the entered movie.
    # imdbid, imdb_api_img = get_imdb_id(search_term) #get usable id from imdb/also a poster
    # moviedb_id = get_id(imdbid)                     #get moviedb id from imdbid
    # movie_genre, movie_title = get_movie_info(moviedb_id)   #get details about the movie

    selected_genre = 35  # movie_genre #can change this when we allow for just a search based on genre
    genre_exclusion = ""  # this will need to be a db call. (SELECT genre FROM genre_exclusions WHERE username = currentuser.username)

    moviedb_list = get_movie_recs(selected_genre)  # , genre_exclusion

    # imdbid, imdb_api_img = get_imdb_id(
    #     search_term
    # )  # get usable id from imdb/also a poster
    # moviedb_id = get_id(imdbid)  # get moviedb id from imdbid
    # movie_genre, movie_title = get_movie_info(moviedb_id)  # get details about the movie

    selected_genre = 35  # movie_genre  # can change this when we allow for just a search based on genre
    genre_exclusion = ""  # this will need to be a db call. (SELECT genre FROM genre_exclusions WHERE username = currentuser.username)

    moviedb_list = get_movie_recs(selected_genre)  # , genre_exclusion

    usename = current_user.username

    saved_movies_list  = [r[0] for r in db.session.query(saved_movies.movieid).filter_by(usename=usename).distinct()]
    ignored_movies_list = [r[0] for r in db.session.query(ignored_movies.ignoredmovieid).filter_by(usename=usename).distinct()]
    movie_exlusions = (
        saved_movies_list + ignored_movies_list
    )  # combine exclusionary fields

    # Have to make the lists sets to compair them easily.
    l1 = set(moviedb_list)
    l2 = set(movie_exlusions)
    rec_set = l1 - l2  # final set of movies to be shown.
    rec_list = list(rec_set)
    print(rec_list)
    return rec_list
