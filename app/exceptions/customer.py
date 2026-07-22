class CustomerException(Exception):
    """Base Customer Exception"""
    pass


class CustomerNotFoundException(CustomerException):

    def __init__(
        self,
        message: str = "Customer not found"
    ):
        self.message = message
        super().__init__(self.message)


class CustomerAlreadyExistsException(CustomerException):

    def __init__(
        self,
        message: str = "Customer already exists"
    ):
        self.message = message
        super().__init__(self.message)