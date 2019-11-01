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

    @staticmethod
    def get_all_data_simplified():
        all_data = Balance._get_all_data()
        data = {}
        lender_ids = {}
        for user_id, user_data in all_data.items():
            data[user_id] = {}
            lender_ids[user_id] = []
            for friend_id, amount in user_data.items():
                if amount <= 0:
                    continue
                lender_ids[user_id].append(friend_id)
                data[user_id][friend_id] = amount

        for user_id in data:
            Balance.__simplify(data, user_id, lender_ids[user_id])

        # convert data back to original unit(divide by 100)
        result = {}
        for user_id, user_data in data.items():
            if not user_data:
                continue
            result[user_id] = {}
            for friend_id, amount in user_data.items():
                result[user_id][friend_id] = amount / 100.0
                if friend_id not in result:
                    result[friend_id] = {}
                result[friend_id][user_id] = -amount / 100.0
        return result

    @staticmethod
    def __simplify(data, user_id, lender_ids):
        # check for transitive debt between lenders and simplify
        n = len(lender_ids)
        for i in range(n):
            lidi = lender_ids[i]
            for j in range(i+1, n):
                lidj = lender_ids[j]
                # if lender is removed
                if lidi not in data[user_id]:
                    break
                # if lender-j owes lender-i, swap lender-j and lender-i
                if lidi in data[lidj]:
                    lidi, lidj = lidj, lidi
                # no transitive debt
                if not lidj in data[lidi]:
                    continue
                # 1--100--> 2--200--> 3       1         2--100--> 3
                #  \                 /   =>    \                 /
                #   -------300------            -------400-------
                if data[user_id][lidi] < data[lidi][lidj]:
                    data[user_id][lidj] += data[user_id][lidi]
                    data[lidi][lidj] -= data[user_id][lidi]
                    del data[user_id][lidi]
                # 1--200--> 2--100--> 3       1--100--> 2         3
                #  \                 /   =>    \                 /
                #   -------300------            -------400-------
                elif data[user_id][lidi] > data[lidi][lidj]:
                    data[user_id][lidj] += data[lidi][lidj]
                    data[user_id][lidi] -= data[lidi][lidj]
                    del data[lidi][lidj]
                # 1--100--> 2--100--> 3       1         2         3
                #  \                 /   =>    \                 /
                #   -------300------            -------400-------
                else:
                    data[user_id][lidj] += data[lidi][lidj]
                    del data[user_id][lidi]
                    del data[lidi][lidj]
