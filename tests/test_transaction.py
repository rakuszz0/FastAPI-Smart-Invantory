def test_get_transactions(client):

    response = client.get(
        "/api/v1/transactions/"
    )

    assert response.status_code == 200


def test_create_transaction(client):

    payload = {

        "customer_id": 1,

        "product_id": 1,

        "quantity": 2

    }

    response = client.post(

        "/api/v1/transactions/",

        json=payload

    )

    assert response.status_code in [
        200,
        201
    ]