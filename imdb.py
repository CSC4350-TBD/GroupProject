import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_imdb_id(search_term):
    IMDB_API_KEY = os.getenv("IMDB_API_KEY")

    imdb_search_url = (
        f"https://imdb-api.com/en/API/SearchMovie/{IMDB_API_KEY}/{search_term}"
    )

    imdb_response = requests.get(imdb_search_url)
    print(imdb_response)
    imdb_j_response = imdb_response.json()

    imdb_id = imdb_j_response["results"][0]["id"]  # First resulting IMDB ID
    imdb_api_img = imdb_j_response["results"][0][
        "image"
    ]  # Image related to the ID (SHould be movie poster)

    return imdb_id, imdb_api_img
