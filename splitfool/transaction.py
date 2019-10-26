from .model import DictModel


class Transaction(DictModel):
    def __init__(self, payee_id: int, friend_ids: int, expense_id: int):
        super().__init__()
        self.payee_id = payee_id
        self.friend_ids = friend_ids
        self.expense_id = expense_id

        # update transaction
        self.__add()

    def __add(self):
        # should be atomic
        print(Transaction.get_all_data())
        for user_id in [self.payee_id, *self.friend_ids]:
            expense_ids = self.get_data(user_id, [])
            expense_ids.append(self.expense_id)
            self._set_data(user_id, expense_ids)

    @staticmethod
    def get_user_data(user_id: int):
        return Transaction.get_data(user_id)
