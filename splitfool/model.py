class DictModel:

    def __init__(self):
        self.uid = self._get_next_id()

    @classmethod
    def _get_next_id(cls) -> dict:
        return len(cls.get_all_data())

    @classmethod
    def get_data(cls, key, default=None):
        return cls.get_all_data().get(key, default)

    @classmethod
    def get_all_data(cls) -> dict:
        if not hasattr(cls, '_data'):
            cls._data = {}
        return cls._data

    @classmethod
    def _set_data(cls, key, val):
        cls.get_all_data()[key] = val

    @classmethod
    def _reset(cls):
        print(cls)
        cls.get_all_data().clear()
