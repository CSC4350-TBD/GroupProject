import requests
import os 
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

def get_imdb_id():       # This will need to be passed the search term, likley the movie that the user liked
    IMDB_API_KEY = os.getenv("IMDB_API_KEY")
    
    search_term = "leon the professional"       #This will need to be replaced with the passed search term
    imdb_search_url = f"https://imdb-api.com/en/API/SearchMovie/{IMDB_API_KEY}/{search_term}"

    imdb_response = requests.get(imdb_search_url)
    print(imdb_response)
    imdb_j_response = imdb_response.json()

    imdb_id = imdb_j_response['results'][0]['id']           #First resulting IMDB ID 
    imdb_api_img = imdb_j_response['results'][0]['image']
    print(imdb_id)
    print(imdb_api_img)

    #for i in imdb_j_response["results"]["id"]:     #Possibly Return more then one result?
        #print(i['results']['id'])
    return imdb_id, imdb_api_img
#get_imdb_id()          #for single function testing