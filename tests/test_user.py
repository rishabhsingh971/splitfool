import unittest
from splitfool import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.name = 'test_user'
        self.phone = '9876543210'
        self.email = 'test@mail.test'
        self.user = User(self.name, self.phone, self.email)

    def test_id(self):
        self.assertIsInstance(self.user.uid, int)

    def test_name(self):
        self.assertEqual(self.user.name, self.name)

    def test_phone(self):
        self.assertEqual(self.user.phone_number, self.phone)

    def test_email(self):
        self.assertEqual(self.user.email, self.email)


if __name__ == '__main__':
    unittest.main()
