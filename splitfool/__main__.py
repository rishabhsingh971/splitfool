import sys
# from getpass import getpass

from .errors import InvalidCredentialsError
from .expense import ExpenseType
from .user import User

user: User = None


def login() -> User:
    print('\n-------- Login --------')
    global user
    while not user:
        user_id = input('user id: ')
        # password = getpass('password: ')
        password = input('password: ')
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


def _add_expense(expense_type: ExpenseType):
    etype = expense_type.name.title()
    print('\n-------- {} Expense --------'.format(etype))
    title = input('Title        : ')
    payee_id = int(input('Payee ID     : '))
    total = float(input('Total Amount : '))
    friend_ids = input('Friend IDs   : ').split(',')
    friend_ids = [int(fid.trim()) for fid in friend_ids]
    shares = None
    if expense_type == ExpenseType.EQUAL:
        shares = ['1']*len(friend_ids)
    else:
        shares = input('{} Shares : '.format(etype)).split(',')

    shares = {
        fid: float(share.trim())
        for fid, share in zip(friend_ids, shares)
    }

    user._add_expense(
        title=title,
        payee_id=payee_id,
        total_amount=total,
        expense_type=expense_type,
        shares=shares
    )


def add_expense():
    login()
    print('\n-------- Expense Type --------')
    options = [
        {
            'desc': ExpenseType.EQUAL.name.title(),
            'fun': lambda: _add_expense(ExpenseType.EQUAL),
        },
        {
            'desc': ExpenseType.EXACT.name.title(),
            'fun': lambda: _add_expense(ExpenseType.EXACT),
        },
        {
            'desc': ExpenseType.PARTS.name.title(),
            'fun': lambda: _add_expense(ExpenseType.PARTS),
        },
        {
            'desc': ExpenseType.PERCENTAGE.name.title(),
            'fun': lambda: _add_expense(ExpenseType.PERCENTAGE),
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


def done():
    print('\n\n+++++++++++ Exit +++++++++++++++')
    sys.exit(0)


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
            'fun': done,
        },
    ]
    while True:
        try:
            print('\n\n============ MAIN ============')
            user_input(options)
        except (KeyboardInterrupt, EOFError):
            try:
                yn = input('\nExit? (y/N): ')
                if yn == 'y':
                    done()
            except (KeyboardInterrupt, EOFError):
                done()
        except Exception:
            pass


if __name__ == "__main__":
    main()
