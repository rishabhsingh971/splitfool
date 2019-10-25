from datetime import datetime
from enum import Enum, auto, unique

from .balance import Balance
from .errors import *
from .transaction import Transaction


@unique
class ExpenseType(Enum):
    EQUAL = auto()
    EXACT = auto()
    PERCENTAGE = auto()
    PARTS = auto()


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
            expense_type: ExpenseType = ExpenseType.EQUAL,
            shares: list = None
    ):
        """add expense

        Arguments:
            title {str} -- expense title
            payee_id {int} -- payee user id
            friend_ids {list} -- list of friend user ids
            total_amount {float} -- total amount

        Keyword Arguments:
            expense_type {ExpenseType} -- type of expense (default: {ExpenseType.EQUAL})
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
        if not self.friend_ids:
            raise InvalidFriendIDsError('No friends specified')
        if self.total_amount <= 0:
            raise InvalidAmountError(
                'Invalid amount - {}'.format(self.total_amount)
            )
        # check valid expense type
        if not isinstance(self.expense_type, ExpenseType):
            raise InvalidExpenseTypeError(
                'Invalid expense type - {}'.format(self.expense_type)
            )
        if self.expense_type == ExpenseType.EQUAL:
            return

        if len(self.friend_ids) != len(self.shares):
            raise InvalidSharesError(
                'Number of shares must by equal to number of friends'
            )
        if not self.shares:
            raise InvalidSharesError('Share of any friend is not given')
        share_sum = 0
        for idx, share in enumerate(self.shares):
            if share < 0:
                raise InvalidSharesError(
                    'Invalid share - {}, for user id - {}'.format(
                        share, self.friend_ids[idx])
                )
            share_sum += share

        if self.expense_type == ExpenseType.PERCENTAGE and share_sum > 100:
            raise InvalidSharesError(
                'Invalid total percentage - {}'.format(share_sum)
            )

        if self.expense_type == ExpenseType.EXACT and share_sum != self.total_amount:
            raise InvalidSharesError(
                'Sum of shares should be equal to total amount, {} != {}'.format(
                    share_sum, self.total_amount)
            )

    def __calculate_amounts(self):
        if self.expense_type == ExpenseType.EQUAL:
            num_friends = len(self.friend_ids)
            return [self.total_amount * round(1.0 / num_friends, 4)] * num_friends

        if self.expense_type == ExpenseType.PERCENTAGE:
            return [
                self.total_amount * round(share / 100, 2) for share in self.shares
            ]

        if self.expense_type == ExpenseType.EXACT:
            return self.shares

        if self.expense_type == ExpenseType.PARTS:
            share_total = sum(self.shares) * 1.0
            return [
                self.total_amount * round(share / share_total, 2) for share in self.shares
            ]

    @staticmethod
    def get_all_data():
        return Expense.__data

    @staticmethod
    def get_by_id(expense_id):
        return Expense.get_all_data().get(expense_id)

    @staticmethod
    def __reset():
        Expense.__data.clear()

    def __repr__(self):
        return '<Expense {}: {}>'.format(self.uid, self.title)
