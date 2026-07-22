class SupplierException(Exception):
    """Base Supplier Exception"""
    pass


class SupplierNotFoundException(SupplierException):

    def __init__(
        self,
        message: str = "Supplier not found"
    ):
        self.message = message
        super().__init__(self.message)


class SupplierAlreadyExistsException(SupplierException):

    def __init__(
        self,
        message: str = "Supplier already exists"
    ):
        self.message = message
        super().__init__(self.message)