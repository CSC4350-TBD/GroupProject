import unittest
from unittest.mock import MagicMock, patch

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from moviedb import get_movie_recs
from imdb import get_imdb_id

class GetImdbIdTest(unittest.TestCase):
    def test_get_imdb_id(self):
       with patch("imdb.requests.get") as mock_requests_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = [
                {
                    "results":[
                         {                           
                            "id":"mockedmovieid",
                               "image":{"mockedmovieimage"}                            
                        }
                    ] 
                }
            ] 
            mock_requests_get.return_value = mock_response
            self.assertEqual(get_imdb_id("Movie Name"),("mockedmovieid",{"mockedmovieimage"}))

class GetMovieRecs(unittest.TestCase):
    def test_get_movie_recs(self):
           with patch("imdb.requests.get") as mock_requests_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = [
              {
                    "results":[
                        {"id":"mockedmovieid1"},
                        {"id":"mockedmovieid2"},
                        {"id":"mockedmovieid3"}
                    ] 
                }
            ] 
            mock_requests_get.return_value = mock_response
            self.assertEqual(get_movie_recs("movie Name"), ["mockedmovieid1","mockedmovieid2","mockedmovieid3"])



if __name__ == '__main__':
    unittest.main()