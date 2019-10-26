class DictModel:
    def __init__(self):
        self.uid = self._get_next_id()

    @classmethod
    def _get_next_id(cls) -> dict:
        return len(cls._get_all_data())

    @classmethod
    def _get_data(cls, key, default=None):
        return cls._get_all_data().get(key, default)

    @classmethod
    def _get_all_data(cls) -> dict:
        if not hasattr(cls, '_data'):
            cls._data = {}
        return cls._data

    @classmethod
    def _set_data(cls, key, val):
        cls._get_all_data()[key] = val

    @classmethod
    def _reset(cls):
        cls._get_all_data().clear()
