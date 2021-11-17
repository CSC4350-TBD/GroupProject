from moviedb import get_movie_info, get_id, get_movie_recs, get_movie_poster
from imdb import get_imdb_id
from model import saved_movies, ignored_movies
from flask_login import current_user
import secrets
from app import db

#This is to abstract all most of the API calls out of routers
def get_recommendation(search_term):  # this is where you will pass the entered movie.
    #moviedb_id = 550 #hardcode ID for testing
    imdbid, imdb_api_img = get_imdb_id(search_term) #get usable id from imdb/also a poster
    moviedb_id = get_id(imdbid)                     #get moviedb id from imdbid
    movie_genre, movie_title = get_movie_info(moviedb_id)   #get details about the movie
    movie_img_url = []

    selected_genre = movie_genre #can change this when we allow for just a search based on genre

    moviedb_list = get_movie_recs(selected_genre)  # , genre_exclusion

    usename = current_user.username

    saved_movies_list  = [r[0] for r in db.session.query(saved_movies.movieid).filter_by(usename=usename).distinct()]
    ignored_movies_list = [r[0] for r in db.session.query(ignored_movies.ignoredmovieid).filter_by(usename=usename).distinct()]
    movie_exlusions = (
        saved_movies_list + ignored_movies_list
    )  # combine exclusionary fields

    for i in saved_movies_list:
        print(i)

    # Have to make the lists sets to compair them easily.
    l1 = set(moviedb_list)
    l2 = set(movie_exlusions)
    l22 = set()

    #have to cast the set from DB to int, as it is returned as string from db
    for i in l2:
        con_to_int = int(i)
        l22.add(con_to_int)

    for i in l22:
        if i in l1:
            l1.remove(i)

    rec_list = list(l1)

    #removing the excluded movies
    for i in rec_list:
        temp = get_movie_poster(i)
        movie_img_url.append(temp)

    print(rec_list)
    return rec_list, movie_img_url