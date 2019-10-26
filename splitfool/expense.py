from datetime import datetime
from enum import Enum, auto, unique

from .balance import Balance
from .errors import InvalidAmountError, InvalidExpenseTypeError, InvalidSharesError
from .model import DictModel
from .transaction import Transaction


@unique
class ExpenseType(Enum):
    EQUAL = auto()
    EXACT = auto()
    PERCENTAGE = auto()
    PARTS = auto()


class Expense(DictModel):

    def __init__(
            self,
            title: str,
            payee_id: int,
            total_amount: float,
            expense_type: ExpenseType,
            shares: dict,
    ):
        """add expense

        Arguments:
            title {str} -- expense title
            payee_id {int} -- payee user id
            total_amount {float} -- total amount
            expense_type {ExpenseType} -- type of expense
            shares {dict} -- map of user id and share
        """
        super().__init__()
        self.title = title
        self.payee_id = payee_id
        self.total_amount = total_amount
        self.expense_type = expense_type
        self.shares = shares

        self.created_at = datetime.now().timestamp
        # validate
        self.__validate()

        # calculate amount per friend
        amounts = self.__calculate_amounts()

        # update expense data
        self.__add()
        # add transaction
        Transaction(payee_id, list(shares.keys()), self.uid)
        # add balance
        Balance(payee_id, amounts)

    def __add(self):
        """update expenses"""
        self._set_data(self.uid, self)

    def __validate(self):
        if not self.shares:
            raise InvalidSharesError('Share of any friend is not given')
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

        share_sum = 0
        for user_id, share in self.shares.items():
            if share < 0:
                raise InvalidSharesError(
                    'Invalid share - {}, for user id - {}'.format(
                        share, user_id)
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
            amount = self.total_amount * round(1.0 / len(self.shares), 4)
            return {
                user_id: amount for user_id in self.shares
            }

        if self.expense_type == ExpenseType.PERCENTAGE:
            return {
                user_id: self.total_amount * round(share / 100, 2) for user_id, share in self.shares.items()
            }

        if self.expense_type == ExpenseType.EXACT:
            return self.shares

        if self.expense_type == ExpenseType.PARTS:
            share_total = sum(self.shares.values()) * 1.0
            return {
                user_id: self.total_amount * round(share / share_total, 2) for user_id, share in self.shares.items()
            }

    @classmethod
    def get_by_id(expense_id):
        return Expense.get_data(expense_id)

    def __repr__(self):
        return '<Expense {}: {}>'.format(self.uid, self.title)
