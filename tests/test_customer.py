def test_get_customers(client):

    response = client.get(
        "/api/v1/customers/"
    )

    assert response.status_code == 200


def test_create_customer(client):

    payload = {

        "name": "Rahmat",

        "email": "rahmat@gmail.com",

        "phone": "081111111111"

    }

    response = client.post(

        "/api/v1/customers/",

        json=payload

    )

    assert response.status_code == 201


def test_customer_detail(client):

    response = client.get(
        "/api/v1/customers/1"
    )

    assert response.status_code in [
        200,
        404
    ]