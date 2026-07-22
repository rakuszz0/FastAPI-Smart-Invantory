def test_get_suppliers(client):

    response = client.get(
        "/api/v1/suppliers/"
    )

    assert response.status_code == 200


def test_create_supplier(client):

    payload = {

        "name": "PT Supplier Indonesia",

        "phone": "08123456789",

        "address": "Jakarta"

    }

    response = client.post(

        "/api/v1/suppliers/",

        json=payload

    )

    assert response.status_code == 201


def test_get_supplier(client):

    response = client.get(
        "/api/v1/suppliers/1"
    )

    assert response.status_code in [
        200,
        404
    ]


def test_update_supplier(client):

    payload = {

        "phone": "082222222222"

    }

    response = client.put(

        "/api/v1/suppliers/1",

        json=payload

    )

    assert response.status_code in [
        200,
        404
    ]


def test_delete_supplier(client):

    response = client.delete(
        "/api/v1/suppliers/1"
    )

    assert response.status_code in [
        200,
        404
    ]