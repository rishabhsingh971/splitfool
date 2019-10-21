# from enum import Enum, unique, auto


# @unique
# class EType(Enum):
#     EQUAL = 'equal'
#     EXACT = 'exact'
#     PERCENTAGE = 'percentage'
#     PARTS = 'parts'


# class User:
#     id = 1

#     def __init__(self, name):
#         self.name = name
#         self.id = User.id
#         User.id += 1


# class Expense:
#     def __init__(self, payee_id, type, borrower_ids, total_amount, expenses=None):
#         self.pa

users = {}
balance = {}


def add_user(user_id: int, user_name: str):
    """add user

    Arguments:
        user_id {int} -- user id
        user_name {str} -- user name

    Raises:
        Exception: User already exists
    """
    if users.get(user_id):
        raise Exception('User already exists')
    users[user_id] = user_name
    print('New user added')


def add_balance(from_user_id: int, to_user_id: int, amount: float):
    """add amount to balance from one user to another

    Arguments:
        from_user_id {int} -- from user id
        to_user_id {int} -- to user id
        amount {float} -- amount to add to balance
    """
    if not from_user_id in balance:
        balance[from_user_id] = {}
    previous_balance = balance.get(from_user_id, {}).get(to_user_id, 0)
    balance[from_user_id][to_user_id] = previous_balance + amount


def add_expense(
        payer_id: int,
        friend_ids: list,
        total_amount: float,
        expense_type: str = 'equal',
        shares: list = None
):
    """add expense

    Arguments:
        payer_id {int} -- payee user id
        type {str} -- type of expense
        friend_ids {list} -- list of friend user ids
        total_amount {float} -- total amount

    Keyword Arguments:
        shares {list} -- share of each friend in case expense
            is not equally distributed (default: {None})
    """
    if not users.get(payer_id):
        raise Exception('Invalid Payer Id - {}'.format(payer_id))
    if not friend_ids:
        raise Exception('No friends specified')
    if total_amount <= 0:
        raise Exception('Invalid amount - {}'.format(total_amount))
    for friend_id in friend_ids:
        if users.get(friend_id):
            continue
        raise Exception('Invalid friend user id - {}'.format(friend_id))
    amounts = None
    if expense_type == 'equal':
        num_borrower = len(friend_ids)
        percentage = round(1.0 / num_borrower, 2)
        amounts = [total_amount*percentage] * num_borrower
    else:
        if len(friend_ids) != len(shares):
            raise Exception('number friends and shares must be equal')
        if not shares:
            raise Exception('share of any friend is not given')

        for idx, share in enumerate(shares):
            if share > 0:
                continue
            raise Exception(
                'Invalid share - {}, for user id - {}'.format(
                    share, friend_ids[idx])
            )
        if expense_type == 'percentage':
            amounts = [
                total_amount * round(share / 100, 2) for share in shares
            ]
        elif expense_type == 'exact':
            amounts = shares
        elif expense_type == 'parts':
            share_total = sum(share_total) * 1.0
            amounts = [
                total_amount * round(share / share_total, 2) for share in shares
            ]
    for friend_id, amount in zip(friend_ids, amounts):
        add_balance(payer_id, friend_id, -amount)
        add_balance(friend_id, payer_id, amount)


# add users
n = 4
for i in range(1, n+1):
    add_user(i, 'user {}'.format(i))
print(users)
add_expense(1, [2], 100)
add_expense(2, [3], 100)
print(balance)
