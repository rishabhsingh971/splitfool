from .user import User
from .expense import ExpenseType
from .errors import InvalidCredentialsError
from getpass import getpass
import sys

user: User = None


def login() -> User:
    print('\n-------- Login --------')
    global user
    while not user:
        user_id = input('user id: ')
        password = getpass('password: ')
        try:
            user = User.login(user_id=user_id, password=password)
        except InvalidCredentialsError as e:
            print(e)

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


def _add_equal_expense():
    print('\n-------- Equal Expense --------')
    title = input('Title        : ')
    payee_id = int(input('Payee ID     : '))
    total = float(input('Total Amount : '))
    friend_ids = input('Friend IDs   : ').split(',')
    friend_ids = [int(fid.trim()) for fid in friend_ids]
    user.add_equal_expense(
        title=title,
        payee_id=payee_id,
        total_amount=total,
        friend_ids=friend_ids
    )


def _add_exact_expense():
    print('\n-------- Exact Expense --------')
    title = input('Title        : ')
    payee_id = int(input('Payee ID     : '))
    total = float(input('Total Amount : '))
    friend_ids = input('Friend IDs   : ').split(',')
    friend_ids = [int(fid.trim()) for fid in friend_ids]
    shares = input('Exact Shares : ').split(',')
    shares = {
        fid: float(share.trim())
        for fid, share in zip(friend_ids, shares)
    }
    user.add_exact_expense(
        title=title,
        payee_id=payee_id,
        total_amount=total,
        shares=shares
    )


def _add_parts_expense():
    print('\n-------- Parts Expense --------')
    title = input('Title        : ')
    payee_id = int(input('Payee ID     : '))
    total = float(input('Total Amount : '))
    friend_ids = input('Friend IDs   : ').split(',')
    friend_ids = [int(fid.trim()) for fid in friend_ids]
    shares = input('Parts Shares : ').split(',')
    shares = {
        fid: float(share.trim())
        for fid, share in zip(friend_ids, shares)
    }
    user.add_parts_expense(
        title=title,
        payee_id=payee_id,
        total_amount=total,
        shares=shares
    )


def _add_percentage_expense():
    print('\n-------- Percentage Expense --------')
    title = input('Title             : ')
    payee_id = int(input('Payee ID         : '))
    total = float(input('Total Amount      : '))
    friend_ids = input('Friend IDs        : ').split(',')
    friend_ids = [int(fid.trim()) for fid in friend_ids]
    shares = input('Percentage Shares : ').split(',')
    shares = {
        fid: float(share.trim())
        for fid, share in zip(friend_ids, shares)
    }
    user.add_percentage_expense(
        title=title,
        payee_id=payee_id,
        total_amount=total,
        shares=shares
    )


def add_expense():
    login()
    print('\n-------- Expense Type --------')
    options = [
        {
            'desc': ExpenseType.EQUAL.name,
            'fun': _add_equal_expense,
        },
        {
            'desc': ExpenseType.EXACT.name,
            'fun': _add_exact_expense,
        },
        {
            'desc': ExpenseType.PARTS.name,
            'fun': _add_parts_expense,
        },
        {
            'desc': ExpenseType.PERCENTAGE.name,
            'fun': _add_percentage_expense,
        },
    ]
    user_input(options)


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
    except (KeyboardInterrupt, EOFError):
        print('\nBYE!!')


if __name__ == "__main__":
    main()
