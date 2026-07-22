from enum import Enum


class UserRole(str, Enum):

    ADMIN = "admin"

    USER = "user"


class TransactionStatus(str, Enum):

    PENDING = "pending"

    SUCCESS = "success"

    FAILED = "failed"


class StockStatus(str, Enum):

    AVAILABLE = "available"

    LOW = "low"

    OUT_OF_STOCK = "out_of_stock"