import unittest
from splitfool import User


class TestEqualExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]

    def test_equal_expense(self):
        self.user.add_equal_expense(
            'expense equal',
            self.user.uid,
            self.friend_ids,
            200
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -66.66, 2: -66.66, 3: -66.66
        })


class TestExactExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]

    def test_exact_expense(self):
        shares = [100, 300, 200]
        self.user.add_exact_expense(
            'expense exact',
            self.user.uid,
            self.friend_ids,
            600,
            shares
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -100, 2: -300, 3: -200
        })


class TestPartsExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]

    def test_parts_expense(self):
        shares = [50, 100, 80]
        self.user.add_parts_expense(
            'expense exact',
            self.user.uid,
            self.friend_ids,
            600,
            shares
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -132.0, 2: -258.0, 3: -210.0
        })


class TestPercentageExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]

    def test_percentage_expense(self):
        shares = [25, 25, 50]
        self.user.add_percentage_expense(
            'expense exact',
            self.user.uid,
            self.friend_ids,
            600,
            shares
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -150.0, 2: -150.0, 3: -300.0
        })


if __name__ == '__main__':
    unittest.main()
