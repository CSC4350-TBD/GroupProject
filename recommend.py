from GroupProject.model import genre_exclusions
from moviedb import get_movie_info, get_id, get_movie_recs
from imdb import get_imdb_id

def get_recommendation(): #this is where you will pass the entered movie.

    search_term = "Dune" #This will need to be changed into a form request later

    imdbid, imdb_api_img = get_imdb_id(search_term) #get usable id from imdb/also a poster
    moviedb_id = get_id(imdbid)                     #get moviedb id from imdbid
    movie_genre, movie_title = get_movie_info(moviedb_id)   #get details about the movie
    
    selected_genre = movie_genre #can change this when we allow for just a search based on genre
    genre_exclusion = ""        #this will need to be a db call. (SELECT genre FROM genre_exclusions WHERE username = currentuser.username)



