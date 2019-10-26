from .model import DictModel


class Balance(DictModel):
    def __init__(self, payee_id, friend_ids, amounts):
        super().__init__()
        self.payee_id = payee_id
        self.friend_ids = friend_ids
        self.amounts = amounts
        self.__add()

    def __add(self):
        for friend_id, amount in zip(self.friend_ids, self.amounts):
            balance = Balance.get_data(self.payee_id, {})
            balance[friend_id] = balance.get(friend_id, 0) - amount
            Balance._set_data(self.payee_id, balance)

            balance = Balance.get_data(friend_id, {})
            balance[self.payee_id] = balance.get(self.payee_id, 0) + amount
            Balance._set_data(friend_id, balance)

    @staticmethod
    def get_user_data(user_id):
        return Balance.get_data(user_id)
