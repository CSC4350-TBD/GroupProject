import unittest
from unittest.mock import Mock
from model import User

class UserModelCase(unittest.TestCase):
    def test_password_hashing(self):
        u1 = User(username='test1')
        u1.set_password('123456')
        u2 = User(username='test1')
        u2.set_password('111111')
        self.assertFalse(u1.check_password('111111'))
        self.assertTrue(u1.check_password('123456'))
        self.assertFalse(u2.check_password('123456'))
        self.assertTrue(u2.check_password('111111'))

if __name__ == '__main__':
    unittest.main()