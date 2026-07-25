import os
from pathlib import Path

import pytest

# Use a file-based SQLite database for tests so connections share the schema
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from fastapi.testclient import TestClient

from app.main import app
from app.core import database as _database

# Ensure all model modules are imported so Base.metadata is populated
import importlib
importlib.import_module("app.models.user")
importlib.import_module("app.models.product")
importlib.import_module("app.models.supplier")
importlib.import_module("app.models.customer")
importlib.import_module("app.models.transaction")
importlib.import_module("app.models.payment")

# Reset schema for each test run so new columns like `transactions.status` are present
if Path("test.db").exists():
    Path("test.db").unlink()

_database.Base.metadata.drop_all(bind=_database.engine)
_database.Base.metadata.create_all(bind=_database.engine)

from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.models.customer import Customer
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.payment import Payment


@pytest.fixture(scope="function")
def client():

    # Clean and reseed DB for each test to avoid order-dependency
    session = Session(bind=_database.engine)
    session.query(Payment).delete()
    session.query(Transaction).delete()
    session.query(Product).delete()
    session.query(Customer).delete()
    session.query(Supplier).delete()

    supplier = Supplier(
        company_name="Default Supplier",
        phone="08123456789",
        address="Jakarta"
    )
    session.add(supplier)

    customer = Customer(
        name="Default Customer",
        email=None,
        phone="08123456789"
    )
    session.add(customer)

    session.commit()

    # Seed a default product attached to the supplier so transactions can reference it
    supplier_id = supplier.id
    product = Product(
        name="Default Product",
        category="General",
        stock=100,
        price=10000,
        supplier_id=supplier_id
    )
    session.add(product)
    session.commit()
    session.close()

    with TestClient(app) as client:
        yield client