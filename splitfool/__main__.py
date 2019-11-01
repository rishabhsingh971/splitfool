from .user import User
from .expense import ExpenseType
from getpass import getpass
import sys

user: User = None


def login() -> User:
    print('\n-------- Login --------')
    global user
    while not user:
        user_id = input('user id: ')
        password = getpass('password: ')
        user = User.login(user_id=user_id, password=password)
    return user


def add_user():
    print('\n-------- Add User --------')
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
    print('Added user, {}'.format(user))


def add_expense():
    print('\n-------- Add Expense --------')


def show_all_users():
    print('\n-------- All Users --------')


def show_user_balances():
    print('\n-------- User Balances --------')


def show_all_balances():
    print('\n-------- All User Balances --------')


def show_user_passbook():
    print('\n-------- User Passbook --------')


def show_simplified_balances():
    print('\n-------- Simplified Balances --------')


def user_input(options):
    for i, option in enumerate(options):
        print('{}. {}'.format(i, option['desc']))
    i = input('Choose option: ')
    if not i.isnumeric() or int(i) < 0 or int(i) >= len(options):
        print('xxxxxxxx INVALID INPUT xxxxxxxx')
    else:
        options[int(i)]['fun']()


def main():
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
        {
            'desc': 'Exit',
            'fun': lambda: sys.exit(0),
        },
    ]
    try:
        while True:
            print('\n\n============ MAIN ============')
            user_input(options)
    except KeyboardInterrupt:
        print('\nBYE!!')


if __name__ == "__main__":
    main()
