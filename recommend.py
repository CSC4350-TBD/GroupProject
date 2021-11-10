from moviedb import get_movie_info, get_id
from imdb import get_imdb_id

def get_recommendation(): #this is where you will pass the entered movie.

    search_term = "Dune" #This will need to be changed into a form request later

    imdbid, imdb_api_img = get_imdb_id(search_term) #get usable id from imdb/also a poster
    moviedb_id = get_id(imdbid)                     #get moviedb id from imdbid
    movie_genre, movie_title = get_movie_info(moviedb_id)   #get details about the movie



