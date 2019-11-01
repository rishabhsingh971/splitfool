from .user import User
from .expense import ExpenseType
from getpass import getpass
import sys

user = None


def login() -> User:
    print('\n-------- Login --------')
    user_id = input('user id: ')
    password = getpass('password: ')
    return User.login(user_id=user_id, password=password)


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
    {
        'desc': 'Exit',
        'fun': lambda: sys.exit(0),
    },
]


def main():
    try:
        while True:
            print('\n\n============ MAIN ============')
            for i, option in enumerate(options):
                print('{}. {}'.format(i, option['desc']))
            i = input('Choose option: ')
            if not i.isnumeric() or int(i) < 0 or int(i) >= len(options):
                print('xxxxxxxx INVALID INPUT xxxxxxxx')
            else:
                options[int(i)]['fun']()
    except KeyboardInterrupt:
        print('\nBYE!!')


if __name__ == "__main__":
    main()
