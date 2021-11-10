from moviedb import get_movie_info, get_id, get_movie_recs
from imdb import get_imdb_id
from model import saved_movies, ignored_movies
from flask_login import current_user
import secrets

def get_recommendation(): #this is where you will pass the entered movie.

    search_term = "Dune" #This will need to be changed into a form request later

    imdbid, imdb_api_img = get_imdb_id(search_term) #get usable id from imdb/also a poster
    moviedb_id = get_id(imdbid)                     #get moviedb id from imdbid
    movie_genre, movie_title = get_movie_info(moviedb_id)   #get details about the movie
    
    selected_genre = movie_genre #can change this when we allow for just a search based on genre
    genre_exclusion = ""        #this will need to be a db call. (SELECT genre FROM genre_exclusions WHERE username = currentuser.username)

    moviedb_list = get_movie_recs(selected_genre, genre_exclusion)

    saved_movies_list = saved_movies.query.filter_by(username=current_user.username).all()
    ignored_movies_list = ignored_movies.query.filter_by(username=current_user.username).all()

    movie_exlusions = saved_movies_list + ignored_movies_list 

    rec_list = [x for x in moviedb_list not in movie_exlusions]

    final_rec = secrets.choice(rec_list)

    return final_rec

def test():
    saved_movies_list = [1,2]
    ignored_movies_list = [7,8]
    moviedb_list = [1,2,3,4,5,6,7,8]


    movie_exlusions = saved_movies_list + ignored_movies_list 
    print(ignored_movies)

    rec_list = [x for x in moviedb_list not in movie_exlusions]
    print(rec_list)
    final_rec = secrets.choice(rec_list)

    print(final_rec)

    return final_rec
test()