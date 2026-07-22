def test_forecasting(client):

    response = client.get(
        "/api/v1/ai/forecast/1"
    )

    assert response.status_code in [
        200,
        404
    ]


def test_recommendation(client):

    response = client.get(
        "/api/v1/ai/recommendation/1"
    )

    assert response.status_code in [
        200,
        404
    ]


def test_anomaly_detection(client):

    response = client.get(
        "/api/v1/ai/anomaly"
    )

    assert response.status_code == 200