import pytest


def test_get_products(client):

    response = client.get(
        "/api/v1/products/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_create_product(client):

    payload = {

        "name": "Keyboard Mechanical",

        "category": "Electronics",

        "stock": 20,

        "price": 750000,

        "supplier_id": 1

    }

    response = client.post(

        "/api/v1/products/",

        json=payload

    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]


def test_get_product_by_id(client):

    response = client.get(
        "/api/v1/products/1"
    )

    assert response.status_code in [
        200,
        404
    ]


def test_update_product(client):

    payload = {

        "stock": 30,

        "price": 800000

    }

    response = client.put(

        "/api/v1/products/1",

        json=payload

    )

    assert response.status_code in [
        200,
        404
    ]


def test_delete_product(client):

    response = client.delete(
        "/api/v1/products/1"
    )

    assert response.status_code in [
        200,
        404
    ]