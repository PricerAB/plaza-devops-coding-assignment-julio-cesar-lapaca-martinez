import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from webapp.src.app import app
import requests

client = TestClient(app)


# ── GET / ──────────────────────────────────────────────

def test_read_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert isinstance(response.json()["message"], str)


def test_read_root_custom_message(monkeypatch):
    monkeypatch.setenv("HELLO_WORLD_MESSAGE", "Hola Star Wars!")
    import importlib
    import webapp.src.app as app_module
    importlib.reload(app_module)
    from fastapi.testclient import TestClient as TC
    c = TC(app_module.app)
    response = c.get("/")
    assert response.status_code == 200
    assert response.json()["message"] != ""


# ── GET /data ──────────────────────────────────────────

def test_get_star_wars_data():
    client = TestClient(app)
    response = client.get("/data")
    assert response.status_code == 200
    assert "name" in response.json()


def test_get_star_wars_data_with_id():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Darth Vader", "height": "202", "mass": "136"}
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/data?id=4")
    assert response.status_code == 200
    assert response.json()["name"] == "Darth Vader"


def test_get_star_wars_data_not_found():
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not found"
    http_error = requests.exceptions.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        response = client.get("/data?id=9999")
    assert response.status_code == 404


def test_get_star_wars_data_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.RequestException("Connection refused")):
        response = client.get("/data?id=1")
    assert response.status_code == 503


def test_get_star_wars_data_server_error():
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    http_error = requests.exceptions.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        response = client.get("/data?id=1")
    assert response.status_code == 500


# ── GET /top-people-by-bmi ─────────────────────────────

MOCK_PEOPLE = [
    {"name": "Luke Skywalker", "height": "172", "mass": "77"},
    {"name": "Darth Vader",    "height": "202", "mass": "136"},
    {"name": "Leia Organa",    "height": "150", "mass": "49"},
    {"name": "Unknown Height", "height": "unknown", "mass": "75"},
    {"name": "Unknown Mass",   "height": "180", "mass": "unknown"},
    {"name": "Jabba the Hutt", "height": "175", "mass": "1,358"},
]


def test_top_people_by_bmi_returns_sorted_list():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_PEOPLE
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    bmis = [p["bmi"] for p in data]
    assert bmis == sorted(bmis, reverse=True)


def test_top_people_by_bmi_skips_unknown_values():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_PEOPLE
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")

    names = [p["name"] for p in response.json()]
    assert "Unknown Height" not in names
    assert "Unknown Mass" not in names


def test_top_people_by_bmi_max_20_results():
    many_people = [
        {"name": f"Person {i}", "height": str(150 + i), "mass": str(50 + i)}
        for i in range(50)
    ]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = many_people
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")

    assert response.status_code == 200
    assert len(response.json()) <= 20


def test_top_people_by_bmi_handles_mass_with_comma():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Jabba the Hutt", "height": "175", "mass": "1,358"}]
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")

    assert response.status_code == 200
    assert response.json()[0]["bmi"] > 0


def test_top_people_by_bmi_empty_list():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")

    assert response.status_code == 200
    assert response.json() == []


def test_top_people_by_bmi_bmi_calculation():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Test", "height": "200", "mass": "80"}]
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")

    # BMI = 80 / (2.0)^2 = 20.0
    assert response.json()[0]["bmi"] == pytest.approx(20.0, abs=0.1)


def test_top_people_by_bmi_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.RequestException("timeout")):
        response = client.get("/top-people-by-bmi")
    assert response.status_code == 503


def test_top_people_by_bmi_api_error():
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Server Error"
    http_error = requests.exceptions.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        response = client.get("/top-people-by-bmi")
    assert response.status_code == 500
