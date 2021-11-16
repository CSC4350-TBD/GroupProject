import unittest
from unittest.mock import MagicMock, patch

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"

from moviedb import get_movie_recs
from imdb import get_imdb_id

class GetImdbIdTest(unittest.TestCase):
    def test_get_imdb_id(self):
       with patch("imdb.requests.get") as mock_requests_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = [
                {},
                {
                    "results":{
                        "hits":[
                            {
                            "id":"mockedmovieid"
                            },
                            {
                            "image":"mockedmovieimage"
                            }
                        ]
                    } 
                }
            ] 
            mock_requests_get.return_value = mock_response
            self.assertEqual(get_imdb_id("movie Name"), None,None)
            self.assertEqual(get_imdb_id("Movie Name 2"),"mockedmovieid","mockedmovieimage"
            )

class GetMovieRecs(unittest.TestCase):
    def test_get_movie_recs(self):
           with patch("imdb.requests.get") as mock_requests_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = [
                {
                    "results":{
                        "hits":[
                            {
                            "id":"mockedmovieid1"
                            }
                        ]
                    } 
                },
                {
                    "results":{
                        "hits":[
                            {
                            "id":"mockedmovieid2"
                            }
                        ]
                    } 
                },
                {
                    "results":{
                        "hits":[
                            {
                            "id":"mockedmovieid3"
                            }
                        ]
                    } 
                }
            ] 
            mock_requests_get.return_value = mock_response
            self.assertEqual(get_movie_recs("movie Name"), ("mockedmovieid1","mockedmoviedid2","mockedmovieid3"))



if __name__ == '__main__':
    unittest.main()