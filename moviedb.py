import requests
import os 
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

#Purpose of this function is to just get the internal ID for themoviedb by telling it the movies' ID from IMDB
def get_id(imdbid):     
    MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")

    id_url = f"https://api.themoviedb.org/3/find/{imdbid}?api_key={MOVIE_DB_API_KEY}&language=en-US&external_source=imdb_id"

    moviedbid_reponse = requests.get(id_url)
    #print(moviedbid_reponse)

    moviedbid_j_reponse = moviedbid_reponse.json()

    moviedb_id = moviedbid_j_reponse['movie_results'][0]['id']

    return moviedb_id



#This will be expanded upon as we decide what information we also want to garther about the movie.
#We will probably need to define a different funciton for the acutual recomendations. 
def get_movie_info(moviedb_id):
    MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")

    info_url =f"https://api.themoviedb.org/3/movie/{moviedb_id}?api_key={MOVIE_DB_API_KEY}&language=en-US"
    movie_info_response = requests.get(info_url)
    #print(movie_info_response)

    movie_info_j_response = movie_info_response.json()

    movie_genre = movie_info_j_response["genres"][0]["name"]
    movie_title = movie_info_j_response["original_title"]
    

    return movie_genre, movie_title