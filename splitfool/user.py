from .balance import Balance
from .expense import Expense
from .transaction import Transaction


class User:
    __num = 1
    __data = {}

    def __init__(self, name: str, phone_number: str = None, email: str = None):
        # assign id
        self.uid = User.__num

        self.name = name
        self.phone_number = phone_number
        self.email = email

        # TODO: sanitize input

        # store user
        User.__data[self.uid] = self
        User.__num += 1

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.__data.get(user_id)

    @staticmethod
    def is_valid(user_id: int):
        return user_id in User.__data

    # DOUBT: how to sync args??
    def add_expense(
            self,
            title: str,
            payee_id: int,
            friend_ids: list,
            total_amount: float,
            expense_type: str = 'equal',
            shares: list = None
    ) -> Expense:
        for friend_id in friend_ids:
            if User.is_valid(friend_id):
                continue
            raise Exception('Invalid friend user id - {}'.format(friend_id))
        return Expense(
            title,
            payee_id,
            friend_ids,
            total_amount,
            expense_type,
            shares
        )

    def get_balance(self):
        return Balance.get_user_data(self.uid)

    def get_transactions(self):
        return Transaction.get_user_data(self.uid)

    def __repr__(self):
        return '<User {} : {}>'.format(self.uid, self.name)
