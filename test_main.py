import pytest
from fastapi.testclient import TestClient
from main import app, init_db, save_record, collect_records,calculate_api

client = TestClient(app)

init_db()

#test calculate function results

def test_calculate_addition():
    assert calculate_api("1 1 +") == 2

def test_calculate_subtraction():
    assert calculate_api("2 1 -") == 1

def test_calculate_multiplication():
    assert calculate_api("2 3 *") == 6

def test_calculate_division():
    assert calculate_api("4 2 /") == 2

def test_calculate_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_api("2 0 /")

def test_calculate_invalid_expression():
    with pytest.raises(ValueError):
        calculate_api("3 +")

# DB test

def test_record_in_db():
    save_record("1 3 +", 4)
    records = collect_records()
    ind = records[-1][0]
    assert len(records) > 0
    assert records[-1] == (ind, "1 3 +", 4)

# Endpoints tests

def test_calculate_valid_expression():
    response = client.post("/calculate", json={"expression": "2 4 +"})
    assert response.status_code == 200
    assert response.json() == {"result": 6}

def test_calculate_invalid_expression():
    response = client.post("/calculate", json={"expression": "2 2 + +"})
    assert response.status_code == 400
    assert "Invalid RPN expression" in response.json()["detail"]

def test_calculate_invalid_token():
    response = client.post("/calculate", json={"expression": "1 2 a"})
    assert response.status_code == 400
    assert "Invalid token in expression" in response.json()["detail"]

def test_export_records():
    response = client.get("/recup")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment; filename=calculator_records.csv" in response.headers["content-disposition"]

# my only problem is that I am not creating a neww temporary database for testing and that i am always adding records when i perform 
# my tests
