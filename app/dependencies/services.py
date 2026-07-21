from app.services.product_service import ProductService
from app.services.supplier_service import SupplierService
from app.services.customer_service import CustomerService
from app.services.transaction_service import TransactionService


def get_product_service():
    return ProductService()


def get_supplier_service():
    return SupplierService()


def get_customer_service():
    return CustomerService()


def get_transaction_service():
    return TransactionService()