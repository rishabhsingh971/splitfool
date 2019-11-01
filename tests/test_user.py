import unittest
from splitfool import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.name = 'test_user'
        self.password = 'pass'
        self.phone = '9876543210'
        self.email = 'test@mail.test'
        self.user = User(
            name=self.name,
            password=self.password,
            phone_number=self.phone,
            email=self.email
        )

    def test_id(self):
        self.assertIsInstance(self.user.uid, int)

    def test_name(self):
        self.assertEqual(self.user.name, self.name)

    def test_password(self):
        self.assertEqual(self.user.password, self.password)

    def test_phone(self):
        self.assertEqual(self.user.phone_number, self.phone)

    def test_email(self):
        self.assertEqual(self.user.email, self.email)

    def test_different_id(self):
        user2 = User(name=self.name, password='pass2')
        self.assertNotEqual(user2.uid, self.user.uid)

    def test_login(self):
        user = User.login(user_id=self.user.uid, password=self.user.password)
        self.assertEqual(user, self.user)


if __name__ == '__main__':
    unittest.main()
