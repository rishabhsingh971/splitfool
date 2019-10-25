from datetime import datetime

from .balance import Balance
from .transaction import Transaction

# from enum import Enum, unique, auto

# @unique
# class ExpenseType(Enum):
#     EQUAL = 'equal'
#     EXACT = 'exact'
#     PERCENTAGE = 'percentage'
#     PARTS = 'parts'


class Expense:
    __balances: dict = {}
    __data: dict = {}
    __num: int = 1

    def __init__(
            self,
            title: str,
            payee_id: int,
            friend_ids: list,
            total_amount: float,
            expense_type: str = 'equal',
            shares: list = None
    ):
        """add expense

        Arguments:
            title {str} -- expense title
            payee_id {int} -- payee user id
            friend_ids {list} -- list of friend user ids
            total_amount {float} -- total amount

        Keyword Arguments:
            expense_type {str} -- type of expense (default: {'equal'})
            shares {list} -- share of each friend in case expense
                is not equally distributed (default: {None})
        """
        # create expense id
        self.uid = Expense.__num

        self.title = title
        self.payee_id = payee_id
        self.friend_ids = friend_ids
        self.total_amount = total_amount
        self.expense_type = expense_type
        self.shares = shares

        self.created_at = datetime.now().timestamp
        # validate
        self.__validate()

        # calculate amount per friend
        amounts = self.__calculate_amounts()

        Expense.__num += 1

        # add transaction
        Transaction(payee_id, friend_ids, self.uid)
        # add balance
        Balance(payee_id, friend_ids, amounts)
        # update expense data
        self.__add()

    def __add(self):
        """update expenses"""
        self.__data[self.uid] = self

    def __validate(self):
        # TODO: use custom exceptions
        if not self.friend_ids:
            raise Exception('No friends specified')
        if self.total_amount <= 0:
            raise Exception('Invalid amount - {}'.format(self.total_amount))

        if self.expense_type == 'equal':
            return

        if len(self.friend_ids) != len(self.shares):
            raise Exception('Number of friends and shares must be equal')
        if not self.shares:
            raise Exception('Share of any friend is not given')
        share_sum = 0
        for idx, share in enumerate(self.shares):
            if share < 0:
                raise Exception(
                    'Invalid share - {}, for user id - {}'.format(
                        share, self.friend_ids[idx])
                )
            share_sum += share

        if self.expense_type == 'percentage' and share_sum > 100:
            raise Exception('Invalid total percentage - {}'.format(share_sum))

        if self.expense_type == 'exact' and share_sum != self.total_amount:
            raise Exception('Sum of shares should be equal to total amount, {} != {}'.format(
                share_sum, self.total_amount))

        # check valid expense type
        # raise Exception('Invalid expense type - {}'.format(self.expense_type))

    def __calculate_amounts(self):
        if self.expense_type == 'equal':
            num_friends = len(self.friend_ids)
            return [self.total_amount * round(1.0 / num_friends, 4)] * num_friends

        if self.expense_type == 'percentage':
            return [
                self.total_amount * round(share / 100, 2) for share in self.shares
            ]

        if self.expense_type == 'exact':
            return self.shares

        if self.expense_type == 'parts':
            share_total = sum(share_total) * 1.0
            return [
                self.total_amount * round(share / share_total, 2) for share in self.shares
            ]

    @staticmethod
    def get_all_data():
        return Expense.__data

    @staticmethod
    def get_by_id(expense_id):
        return Expense.get_all_data().get(expense_id)

    def __repr__(self):
        return '<Expense {}: {}>'.format(self.uid, self.title)
