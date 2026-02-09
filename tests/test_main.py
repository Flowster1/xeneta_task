from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_capacity_valid_range():
    """
    Test a valid request.
    Expectation: 200 OK and a non-empty list.
    """
    response = client.get("/capacity?date_from=2024-01-01&date_to=2024-01-31")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        item = data[0]
        assert "week_start_date" in item
        assert "week_no" in item
        assert "offered_capacity_teu" in item
        assert isinstance(item["offered_capacity_teu"], int)


def test_get_capacity_no_data():
    """
    Test a date range where no data exists.
    Expectation: 200 OK, but an empty list [].
    """
    response = client.get("/capacity?date_from=2030-01-01&date_to=2030-02-01")

    assert response.status_code == 200
    assert response.json() == []



def test_get_capacity_invalid_date_logic():
    """
    Test start_date > end_date.
    Expectation: 400 Bad Request (Custom Error).
    """
    response = client.get("/capacity?date_from=2024-02-01&date_to=2024-01-01")

    assert response.status_code == 400
    error_data = response.json()
    assert error_data["error_code"] == "INVALID_DATE_RANGE"


def test_get_capacity_bad_input_type():
    """
    Test sending text instead of a date.
    Expectation: 422 Unprocessable Entity (FastAPI default).
    """
    response = client.get("/capacity?date_from=not-a-date&date_to=2024-01-01")

    assert response.status_code == 422
