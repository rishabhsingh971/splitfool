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
            balance = Balance._get_data(self.payee_id, {})
            balance[friend_id] = balance.get(friend_id, 0) - amount
            if balance[friend_id] == 0:
                del balance[friend_id]
            Balance._set_data(self.payee_id, balance)

            balance = Balance._get_data(friend_id, {})
            balance[self.payee_id] = balance.get(self.payee_id, 0) + amount
            if balance[self.payee_id] == 0:
                del balance[self.payee_id]
            Balance._set_data(friend_id, balance)

    @staticmethod
    def get_user_data(user_id):
        data = Balance._get_data(user_id, {}).copy()
        for user_id, amount in data.items():
            data[user_id] = amount / 100.0
        return data

    @staticmethod
    def get_all_data():
        all_data = Balance._get_all_data()
        data = {}
        for user_id, user_data in all_data.items():
            data[user_id] = {}
            for friend_id, amount in user_data.items():
                data[user_id][friend_id] = amount / 100.0
        return data
