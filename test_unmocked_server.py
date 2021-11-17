import unittest
from model import User

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"

class UserModelCase(unittest.TestCase):    
    def test_password_hashing1(self):
        u1 = User(username='test1')
        u1.set_password('123456')
        self.assertTrue(u1.check_password('123456'))
    def test_password_hashing2(self):
        u2 = User(username='test2')
        u2.set_password('111111')
        self.assertTrue(u2.check_password('111111'))


   
# class ImdbHelpTest(unittest.TestCase):




if __name__ == '__main__':
    unittest.main()