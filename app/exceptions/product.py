class ProductException(Exception):
    """Base Product Exception"""
    pass


class ProductNotFoundException(ProductException):

    def __init__(
        self,
        message: str = "Product not found"
    ):
        self.message = message
        super().__init__(self.message)


class ProductAlreadyExistsException(ProductException):

    def __init__(
        self,
        message: str = "Product already exists"
    ):
        self.message = message
        super().__init__(self.message)


class ProductOutOfStockException(ProductException):

    def __init__(
        self,
        message: str = "Product stock is insufficient"
    ):
        self.message = message
        super().__init__(self.message)