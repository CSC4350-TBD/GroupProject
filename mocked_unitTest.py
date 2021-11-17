import unittest
from unittest.case import TestCase
from unittest.mock import MagicMock, patch

import sys
import os


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model import*
from router import*

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class UpdateSaveDBIDsTests(unittest.TestCase):
    def setUp(self):
        self.db_mock = [saved_movies(movieid="foo", usename="Yul")]

    def mock_add_to_db(self, movie):
        self.db_mock.append(movie)

    def mock_delete_from_db(self, movie):
        self.db_mock = [
            entry for entry in self.db_mock if entry.movieid != movie.movieid
        ]

    def mock_db_commit(self):
        pass

    def test_update_db_ids_for_user(self):
        with patch("router.saved_movies.query") as mock_query:
            with patch("router.db.session.add", self.mock_add_to_db):
                with patch("router.db.session.delete", self.mock_delete_from_db):
                    with patch("router.db.session.commit", self.mock_db_commit):
                        mock_filtered = MagicMock()
                        mock_filtered.all.return_value = self.db_mock
                        mock_filtered.filter.return_value = [
                            saved_movies(movieid="hup", usename="Yul")
                        ]
                        mock_query.filter_by.return_value = mock_filtered
                        update_db_ids_for_user("Yul", {"foo"})
                        self.assertEqual(len(self.db_mock), 1)
                        self.assertEqual(self.db_mock[0].movieid, "foo")

                
                        update_db_ids_for_user("Yul", {"foo", "hup"})
                        self.assertEqual(len(self.db_mock), 2)
                        self.assertEqual(self.db_mock[0].movieid, "foo")
                        self.assertEqual(self.db_mock[1].movieid, "hup")

                    
                        update_db_ids_for_user("Yul", {"foo", "baz"})
                        self.assertEqual(len(self.db_mock), 2)
                        self.assertEqual(self.db_mock[0].movieid, "foo")
                        self.assertEqual(self.db_mock[1].movieid, "baz")



class GetMoviedbTests(unittest.TestCase):
    def test_get_id(self):
        with patch("moviedb.requests.get") as mock_requests_get:
            mock_response = MagicMock()
          
            mock_response.json.side_effect = [
                {},
                {
                    "movie_results": {
                        "id": [
                            {
                                550
                                }
                            
                        ]
                    }
                },
            ]
            mock_requests_get.return_value = mock_response

            self.assertEqual(get_id("Movie id"), None)
            self.assertEqual(
                get_id("moviebd_id2"),
                550,
            )

if __name__ == "__main__":
    unittest.main()