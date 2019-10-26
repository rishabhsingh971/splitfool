class BaseError(Exception):
    pass


class InvalidFriendIDsError(BaseError):
    pass


class InvalidSharesError(BaseError):
    pass


class InvalidAmountError(BaseError):
    pass


class InvalidExpenseTypeError(BaseError):
    pass
