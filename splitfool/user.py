from .balance import Balance
from .expense import Expense, ExpenseType
from .errors import InvalidFriendIDsError, InvalidCredentialsError
from .model import DictModel
from .transaction import Transaction


class User(DictModel):
    def __init__(
            self,
            name: str,
            password: str,
            phone_number: str = None,
            email: str = None
    ):
        super().__init__()

        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.email = email

        self.__add()
        # TODO: sanitize input

    def __add(self):
        User._set_data(self.uid, self)

    @staticmethod
    def get_user_by_id(user_id: int):
        return User._get_data(user_id)

    @staticmethod
    def is_valid(user_id: int):
        return user_id in User._get_all_data()

    def __add_expense(
            self,
            title: str,
            payee_id: int,
            total_amount: float,
            expense_type: ExpenseType,
            shares: dict,
    ) -> Expense:
        for friend_id in shares.keys():
            if User.is_valid(friend_id):
                continue
            raise InvalidFriendIDsError(
                'Invalid friend user id - {}'.format(friend_id)
            )
        Expense(
            title=title,
            payee_id=payee_id,
            total_amount=total_amount,
            expense_type=expense_type,
            shares=shares,
            created_by=self.uid,
        )

    def add_equal_expense(
            self,
            title: str,
            payee_id: int,
            total_amount: float,
            friend_ids: list,
    ) -> Expense:
        self.__add_expense(
            title=title,
            payee_id=payee_id,
            total_amount=total_amount,
            expense_type=ExpenseType.EQUAL,
            shares={friend_id: 1 for friend_id in friend_ids},
        )

    def add_exact_expense(
            self,
            title: str,
            payee_id: int,
            total_amount: float,
            shares: dict,
    ) -> Expense:
        self.__add_expense(
            title=title,
            payee_id=payee_id,
            total_amount=total_amount,
            expense_type=ExpenseType.EXACT,
            shares=shares,
        )

    def add_parts_expense(
            self,
            title: str,
            payee_id: int,
            total_amount: float,
            shares: list,
    ) -> Expense:
        self.__add_expense(
            title=title,
            payee_id=payee_id,
            total_amount=total_amount,
            expense_type=ExpenseType.PARTS,
            shares=shares,
        )

    def add_percentage_expense(
            self,
            title: str,
            payee_id: int,
            total_amount: float,
            shares: list,
    ) -> Expense:
        self.__add_expense(
            title=title,
            payee_id=payee_id,
            total_amount=total_amount,
            expense_type=ExpenseType.PERCENTAGE,
            shares=shares,
        )

    def get_expenses(self):
        return Expense.get_user_data(self.uid)

    def get_balance(self):
        return Balance.get_user_data(self.uid)

    def get_transactions(self):
        return Transaction.get_user_data(self.uid)

    @staticmethod
    def get_all_balances():
        return Balance.get_all_data()

    @staticmethod
    def get_all_balances_simplified():
        return Balance.get_all_data_simplified()

    @staticmethod
    def _reset_all():
        Balance._reset()
        Expense._reset()
        Transaction._reset()
        User._reset()

    @staticmethod
    def login(user_id: int, password: str):
        print(User._get_all_data())
        user = User.get_user_by_id(user_id)
        print(user.password, password, user.password == password)
        if not user or user.password != password:
            raise InvalidCredentialsError('Invalid user id or password')
        return user

    def __repr__(self):
        return '<User {} : {}>'.format(self.uid, self.name)
