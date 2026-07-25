def test_register(client):

    payload = {

        "fullname": "Rahmat",

        "email": "rahmat@gmail.com",

        "password": "Password123",

        "confirm_password": "Password123"

    }

    response = client.post(

        "/api/v1/auth/register",

        json=payload

    )

    assert response.status_code in [
        201,
        409
    ]


def test_login(client):

    payload = {

        "email": "rahmat@gmail.com",

        "password": "Password123"

    }

    response = client.post(

        "/api/v1/auth/login",

        json=payload

    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def test_profile(client):

    login = client.post(

        "/api/v1/auth/login",

        json={

            "email": "rahmat@gmail.com",

            "password": "Password123"

        }

    )

    token = login.json()["access_token"]

    response = client.get(

        "/api/v1/auth/me",

        headers={

            "Authorization": f"Bearer {token}"

        }

    )

    assert response.status_code == 200
