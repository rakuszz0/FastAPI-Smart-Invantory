from enum import Enum


class UserRole(str, Enum):

    SUPER_ADMIN = "super_admin"

    ADMIN = "admin"

    STAFF = "staff"

    USER = "user"


class TransactionStatus(str, Enum):

    PENDING = "pending"

    SUCCESS = "success"

    FAILED = "failed"


class StockStatus(str, Enum):

    AVAILABLE = "available"

    LOW = "low"

    OUT_OF_STOCK = "out_of_stock"
