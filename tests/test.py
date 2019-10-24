import unittest
from splitfool import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('test user', '9876543210', 'test@mail.test')

    def test_id(self):
        self.assertIsInstance(self.user.uid, int)


if __name__ == '__main__':
    unittest.main()
