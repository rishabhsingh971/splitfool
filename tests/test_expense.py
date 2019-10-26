import unittest
from splitfool import User


class TestExpense(unittest.TestCase):
    def setUp(self):
        User._reset_all()
        n = 5
        users = []
        for i in range(1, n+1):
            user = User('username {}'.format(i))
            users.append(user)
        self.user = users[0]

    def check_function(self, function_name):
        self.assertTrue(hasattr(self.user, function_name))
        self.assertTrue(callable(getattr(self.user, function_name)))

    def check_last_expense(self, props):
        last_expense = self.user.get_expenses()[-1]
        for key, val in props.items():
            self.assertIn(key, last_expense)
            self.assertEqual(val, last_expense[key])


class TestEqualExpense(TestExpense):
    def test_user_can_add_equal_expense(self):
        self.check_function('add_equal_expense')

    def test_equal_expense(self):
        props = {
            'title': 'expense equal',
            'payee_id': self.user.uid,
            'total_amount': 200
        }
        self.user.add_equal_expense(
            **props,
            friend_ids=[1, 2, 3],
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -66.66, 2: -66.67, 3: -66.67
        })
        self.check_last_expense(props)

    def test_self_expense(self):
        self.user.add_equal_expense(
            title='expense equal',
            payee_id=self.user.uid,
            friend_ids=[1, 2, 3, self.user.uid],
            total_amount=200
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -50.0, 2: -50.0, 3: -50.0
        })


class TestExactExpense(TestExpense):
    def test_user_can_add_exact_expense(self):
        self.check_function('add_exact_expense')

    def test_exact_expense(self):
        props = {
            'title': 'expense exact',
            'payee_id': self.user.uid,
            'total_amount': 600,
            'shares': {1: 100, 2: 300, 3: 200}
        }

        self.user.add_exact_expense(
            **props
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -100, 2: -300, 3: -200
        })
        self.check_last_expense(props)


class TestPartsExpense(TestExpense):
    def test_user_can_add_parts_expense(self):
        self.check_function('add_parts_expense')

    def test_parts_expense(self):
        props = {
            'title': 'expense exact',
            'payee_id': self.user.uid,
            'total_amount': 600,
            'shares': {1: 50, 2: 100, 3: 80}
        }

        self.user.add_parts_expense(
            **props
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -132.0, 2: -258.0, 3: -210.0
        })
        self.check_last_expense(props)


class TestPercentageExpense(TestExpense):
    def test_user_can_add_percentage_expense(self):
        self.check_function('add_percentage_expense')

    def test_percentage_expense(self):
        props = {
            'title': 'expense exact',
            'payee_id': self.user.uid,
            'total_amount': 600,
            'shares': {1: 25, 2: 25, 3: 50}
        }

        self.user.add_percentage_expense(
            **props
        )
        self.assertDictEqual(self.user.get_balance(), {
            1: -150.0, 2: -150.0, 3: -300.0
        })
        self.check_last_expense(props)


if __name__ == '__main__':
    unittest.main()
