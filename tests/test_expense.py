import unittest
from splitfool import User


class TestEqualExpense(unittest.TestCase):
    def setUp(self):
        User._reset_all()
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.friend_ids = list(map(lambda user: user.uid, users[1:-1]))
        self.user = users[0]

    def test_user_can_add_equal_expense(self):
        self.assertTrue(hasattr(self.user, 'add_equal_expense'))
        self.assertTrue(callable(getattr(self.user, 'add_equal_expense')))

    def test_equal_expense(self):
        self.user.add_equal_expense(
            title='expense equal',
            payee_id=self.user.uid,
            friend_ids=self.friend_ids,
            total_amount=200
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -66.66, 2: -66.66, 3: -66.66
        })

    def test_self_expense(self):
        self.user.add_equal_expense(
            title='expense equal',
            payee_id=self.user.uid,
            friend_ids=[*self.friend_ids, self.user.uid],
            total_amount=200
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -50.0, 2: -50.0, 3: -50.0
        })


class TestExactExpense(unittest.TestCase):
    def setUp(self):
        User._reset_all()
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.user = users[0]

    def test_user_can_add_exact_expense(self):
        self.assertTrue(hasattr(self.user, 'add_exact_expense'))
        self.assertTrue(callable(getattr(self.user, 'add_exact_expense')))

    def test_exact_expense(self):
        shares = {1: 100, 2: 300, 3: 200}
        self.user.add_exact_expense(
            title='expense exact',
            payee_id=self.user.uid,
            total_amount=600,
            shares=shares,
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -100, 2: -300, 3: -200
        })


class TestPartsExpense(unittest.TestCase):
    def setUp(self):
        User._reset_all()
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.user = users[0]

    def test_user_can_add_parts_expense(self):
        self.assertTrue(hasattr(self.user, 'add_parts_expense'))
        self.assertTrue(callable(getattr(self.user, 'add_parts_expense')))

    def test_parts_expense(self):
        shares = {1: 50, 2: 100, 3: 80}
        self.user.add_parts_expense(
            title='expense parts',
            payee_id=self.user.uid,
            total_amount=600,
            shares=shares,
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -132.0, 2: -258.0, 3: -210.0
        })


class TestPercentageExpense(unittest.TestCase):
    def setUp(self):
        User._reset_all()
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.user = users[0]

    def test_user_can_add_percentage_expense(self):
        self.assertTrue(hasattr(self.user, 'add_percentage_expense'))
        self.assertTrue(callable(getattr(self.user, 'add_percentage_expense')))

    def test_percentage_expense(self):
        shares = {1: 25, 2: 25, 3: 50}
        self.user.add_percentage_expense(
            title='expense percentage',
            payee_id=self.user.uid,
            total_amount=600,
            shares=shares,
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -150.0, 2: -150.0, 3: -300.0
        })


if __name__ == '__main__':
    unittest.main()
