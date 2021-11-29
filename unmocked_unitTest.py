import unittest
from unittest.mock import MagicMock, patch

import sys
import os

from flask import Flask, request, Response
from router import app


INPUT = "IMPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class UserLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_login_invalid_username(self):
        rv = self.app.post('/login', data=dict(username="007", password="006"))
        self.assertIn('/login', rv.get_data().decode())
        self.assertEqual(302, rv.status_code)

    def test_login_invalid_password(self):
        rv = self.app.post('/login', data=dict(username="yul", password="006"))
        self.assertIn('/login', rv.get_data().decode())
        self.assertEqual(302, rv.status_code)

    def test_login_valid_username_and_password(self):
        rv = self.app.post('/login', data=dict(username="Yul", password="123"))
        print(rv)
        self.assertIn('/index', rv.get_data().decode())
        self.assertEqual(302, rv.status_code)





if __name__ == "__main__":
    unittest.main()
