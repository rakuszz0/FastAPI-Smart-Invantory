class TransactionException(Exception):
    """Base Transaction Exception"""
    pass


class TransactionNotFoundException(TransactionException):

    def __init__(
        self,
        message: str = "Transaction not found"
    ):
        self.message = message
        super().__init__(self.message)


class InvalidTransactionException(TransactionException):

    def __init__(
        self,
        message: str = "Invalid transaction"
    ):
        self.message = message
        super().__init__(self.message)