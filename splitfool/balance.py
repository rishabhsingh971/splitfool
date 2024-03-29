from .model import DictModel


class Balance(DictModel):
    def __init__(self, payee_id: int, amounts: dict):
        super().__init__()
        self.payee_id = payee_id
        self.amounts = amounts
        self.__add()

    def __add(self):
        for friend_id, amount in self.amounts.items():
            if friend_id == self.payee_id:
                continue
            balance = Balance.get_data(self.payee_id, {})
            balance[friend_id] = balance.get(friend_id, 0) - amount
            if balance[friend_id] == 0:
                del balance[friend_id]
            Balance._set_data(self.payee_id, balance)

            balance = Balance.get_data(friend_id, {})
            balance[self.payee_id] = balance.get(self.payee_id, 0) + amount
            if balance[self.payee_id] == 0:
                del balance[self.payee_id]
            Balance._set_data(friend_id, balance)

    @staticmethod
    def get_user_data(user_id):
        return Balance.get_data(user_id)
