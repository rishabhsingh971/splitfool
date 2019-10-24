import unittest
from splitfool import User


class TestExpense(unittest.TestCase):
    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]

    def test_equal_expense(self):
        self.user.add_expense('uber', self.user.uid, self.friend_ids, 200)
        self.assertDictEqual(self.user.get_balance(), {
            2: -66.66, 3: -66.66, 4: -66.66
        })


if __name__ == '__main__':
    unittest.main()
