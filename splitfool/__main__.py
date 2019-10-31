from .user import User
from .expense import ExpenseType
from getpass import getpass


def login():
    print('-------- Login --------')
    user_id = input('user id: ')
    password = getpass('password: ')
    user = User.get_user_by_id(user_id)
    if not user or user.password != password:
        print('Invalid user id or password')
        return False
    return True


def add_user():
    print('-------- User Details --------')
    name = input('Name         : ')
    password = input('Password     : ')
    phone = input('Phone Number : ')
    email = input('Email ID     : ')
    user = User(
        name=name,
        password=password,
        phone_number=phone,
        email=email
    )
    print('Added user, id : {}'.format(user.uid))


def add_expense():
    pass


def show_all_users():
    pass


def show_user_balances():
    pass


def show_all_balances():
    pass


def show_user_passbook():
    pass


def show_simplified_balances():
    pass


options = [
    {
        'desc': 'Add User',
        'fun': add_user,
    },
    {
        'desc': 'Add Expense',
        'fun': add_expense,
    },
    {
        'desc': 'Show all User',
        'fun': show_all_users,
    },
    {
        'desc': 'Show User Balances',
        'fun': show_user_balances,
    },
    {
        'desc': 'Show All Balances',
        'fun': show_all_balances,
    },
    {
        'desc': 'Show User Passbook',
        'fun': show_user_passbook,
    },
    {
        'desc': 'Show simplified balances',
        'fun': show_simplified_balances,
    },
]