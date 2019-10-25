class Transaction:
    __data: dict = {}
    __num: int = 1

    def __init__(self, payee_id: int, friend_ids: int, expense_id: int):
        self.uid = Transaction.__num
        self.payee_id = payee_id
        self.friend_ids = friend_ids
        self.expense_id = expense_id

        # update transaction
        self.__add()
        Transaction.__num += 1

    def __add(self):
        # should be atomic
        for user_id in [self.payee_id, *self.friend_ids]:
            expense_ids = Transaction.__data.get(user_id, [])
            expense_ids.append(self.expense_id)
            Transaction.__data[user_id] = expense_ids

    @staticmethod
    def get_all_data():
        return Transaction.__data

    @staticmethod
    def get_user_data(user_id: int):
        return Transaction.__data.get(user_id)

    @staticmethod
    def __reset():
        Transaction.__data.clear()
