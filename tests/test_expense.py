import unittest
from splitfool import User, ExpenseType


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
        self.user.add_expense(
            'expense equal',
            self.user.uid,
            self.friend_ids,
            200
        )
        print(self.user.get_all_data())
        print(self.user.get_balance())
        self.assertDictEqual(self.user.get_balance(), {
            1: -66.66, 2: -66.66, 3: -66.66
        })


class TestExactExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('set up')
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]
        print(self.user, self.friend_ids)

    def test_exact_expense(self):
        shares = [100, 300, 200]
        self.user.add_expense(
            'expense exact',
            self.user.uid,
            self.friend_ids,
            600,
            ExpenseType.EXACT,
            shares
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -100, 2: -300, 3: -200
        })


class TestPartsExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('set up')
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]
        print(self.user, self.friend_ids)

    def test_parts_expense(self):
        shares = [50, 100, 80]
        self.user.add_expense(
            'expense exact',
            self.user.uid,
            self.friend_ids,
            600,
            ExpenseType.PARTS,
            shares
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -132.0, 2: -258.0, 3: -210.0
        })


class TestPercentageExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('set up')
        User._reset_all()

    def setUp(self):
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]
        print(self.user, self.friend_ids)

    def test_percentage_expense(self):
        shares = [25, 25, 50]
        self.user.add_expense(
            'expense exact',
            self.user.uid,
            self.friend_ids,
            600,
            ExpenseType.PERCENTAGE,
            shares
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -150.0, 2: -150.0, 3: -300.0
        })


if __name__ == '__main__':
    unittest.main()
