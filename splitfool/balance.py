class Balance:
    __data: dict = {}
    __num: int = 1

    def __init__(self, payee_id, friend_ids, amounts):
        self.uid = Balance.__num
        self.payee_id = payee_id
        self.friend_ids = friend_ids
        self.amounts = amounts
        self.__add()
        Balance.__num += 1

    def __add(self):
        for friend_id, amount in zip(self.friend_ids, self.amounts):
            balance = Balance.__data.get(self.payee_id, {})
            balance[friend_id] = balance.get(friend_id, 0) - amount
            Balance.__data[self.payee_id] = balance

            balance = Balance.__data.get(friend_id, {})
            balance[self.payee_id] = balance.get(self.payee_id, 0) + amount
            Balance.__data[friend_id] = balance

    @staticmethod
    def get_all_data():
        return Balance.__data

    @staticmethod
    def get_user_data(user_id):
        return Balance.get_all_data().get(user_id)
