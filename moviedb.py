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
def get_movie_info(moviedb_id):
    MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")

    info_url =f"https://api.themoviedb.org/3/movie/{moviedb_id}?api_key={MOVIE_DB_API_KEY}&language=en-US"
    movie_info_response = requests.get(info_url)
    #print(movie_info_response)

    movie_info_j_response = movie_info_response.json()

    movie_genre = movie_info_j_response["genres"][0]["id"]
    movie_title = movie_info_j_response["original_title"]
    

    return movie_genre, movie_title

def get_movie_poster(moviedb_id):
    MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")
    img_base = "https://image.tmdb.org/t/p/original"
    img_url = f"https://api.themoviedb.org/3/movie/{moviedb_id}/images?api_key={MOVIE_DB_API_KEY}&language=en-US&include_image_language=en"

    img_response = requests.get(img_url)
    img_j_response = img_response.json()

    img_ext = img_j_response["posters"][0]["file_path"]

    movie_image_url = img_base + img_ext

    return movie_image_url


def get_detailed_info(moviedb_id):
    MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")

    info_url =f"https://api.themoviedb.org/3/movie/{moviedb_id}?api_key={MOVIE_DB_API_KEY}&language=en-US"
    cast_url =f"https://api.themoviedb.org/3/movie/{moviedb_id}/credits?api_key={MOVIE_DB_API_KEY}&language=en-US"
    movie_info_response = requests.get(info_url)
    cast_url_response = requests.get(cast_url)

    #print(movie_info_response)

    movie_info_j_response = movie_info_response.json()
    cast_url_j_response = cast_url_response.json()

    movie_img_url = "https://image.tmdb.org/t/p/original"

    movie_title = movie_info_j_response["original_title"]
    movie_genre = movie_info_j_response["genres"][0]["name"]
    movie_desc = movie_info_j_response["overview"]
    movie_runtime = movie_info_j_response["runtime"]
    movie_rating = movie_info_j_response["vote_average"]
    movie_img_ext = movie_info_j_response["backdrop_path"]
    movie_img = movie_img_url + movie_img_ext

    cast_limit = 3
    cast = []
    director = ""

    for i in cast_url_j_response["cast"]:
        if cast_limit > 0:
            cast.append(i["name"])
        cast_limit -=1

    for i in cast_url_j_response["crew"]:
        if i["job"]=="Director":
            director = i["name"]
            break
        
    return movie_title, movie_img, movie_genre, movie_desc, movie_runtime, movie_rating, cast, director


    

def get_movie_recs(selected_genre): #genre_exclusion, 
    MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")

    # possibly should add &with_keywords={keywords} if we want to add a keyword field
    #search_url = f"https://api.themoviedb.org/3/discover/movie?api_key={MOVIE_DB_API_KEY}&language=en-US&sort_by=popularity.desc&page=1&with_genres={selected_genre}" #&without_genres={genre_exclusion}
    search_url = f"https://api.themoviedb.org/3/discover/movie?api_key={MOVIE_DB_API_KEY}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={selected_genre}&with_watch_monetization_types=flatrate"
    search_response = requests.get(search_url)

    search_j_response = search_response.json()
    print("THIS IS MOVIEDB>PY")

    movie_list = []

    for i in search_j_response["results"]:
        movie_list.append(i["id"])
    print(movie_list)
    print("THIS IS MOVIEDB>PY")
    return movie_list