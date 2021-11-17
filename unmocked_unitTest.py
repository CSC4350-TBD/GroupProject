import unittest
from unittest.mock import MagicMock, patch

import sys
import os

from moviedb import get_movie_info


INPUT = "IMPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class BasicTests(unittest.TestCase):
    def setUp(self):
          self.success_test_params = [
            {
                INPUT: {},
                EXPECTED_OUTPUT: (None, None),
            },
            {
                INPUT: {"original_title": "Movie title"},
                EXPECTED_OUTPUT: ("Movie Title", None),
            },
            {
                INPUT: {
                    "original_title": "Movie title",
                    "movie_genre": {"Movie genre" : "genres"},
                    "movie_img" : {"images": [{"url": "image_url"}]}
                    
                },
                EXPECTED_OUTPUT: (
                    "Movie title",
                     "genres",
                    "image_url",
                    
                ),
            },
        ]

    def test_extract_movie_title(self):
        for test in self.success_test_params:
            self.assertEqual(get_movie_info(test[INPUT]), test[EXPECTED_OUTPUT])
        

   



if __name__ =='__main__':
    unittest.main()