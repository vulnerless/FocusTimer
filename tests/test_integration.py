"""Integration tests for the Flask API (user stories US7-US10).

Each test sends real HTTP requests through the Flask test client, so the
routes in app.py and the logic in timer_core.py are tested together.
Each test docstring states the test method, purpose and expected result.
"""

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def add_task(client, title="Read chapter 3"):
    return client.post("/api/tasks", json={"title": title})


# US7 - Change timer durations (BVA + EP)
def test_us7_ac1_valid_boundaries_accepted(client):
    """Method: Integration
    Purpose: BVA on valid edges 1 and 60.
    Expected: 200 and values saved.
    """
    for value in (1, 60):
        body = {"work": value, "break": value}
        res = client.post("/api/settings", json=body)
        assert res.status_code == 200
        assert res.get_json()["work_minutes"] == value
        assert res.get_json()["remaining"] == value * 60


def test_us7_ac2_invalid_values_rejected(client):
    """Method: Integration
    Purpose: BVA 0/61 + invalid classes (text, missing).
    Expected: 400.
    """
    for body in ({"work": 0, "break": 5}, {"work": 61, "break": 5},
                 {"work": 25, "break": 0}, {"work": "ten", "break": 5}, {}):
        res = client.post("/api/settings", json=body)
        assert res.status_code == 400
    assert client.get("/api/timer").get_json()["work_minutes"] == 25


# US8 - Add a task
def test_us8_ac1_add_task_appears_in_list(client):
    """Method: Integration
    Purpose: a new task is saved.
    Expected: 201 and task in the list.
    """
    res = add_task(client)
    assert res.status_code == 201
    titles = [t["title"] for t in client.get("/api/tasks").get_json()]
    assert titles == ["Read chapter 3"]


def test_us8_ac2_empty_or_long_title_rejected(client):
    """Method: Integration
    Purpose: EP on titles (empty, spaces, 101 chars).
    Expected: 400.
    """
    for title in ("", "   ", "a" * 101):
        assert add_task(client, title).status_code == 400
    assert add_task(client, "a" * 100).status_code == 201


# US9 - Complete a task
def test_us9_ac1_complete_marks_done(client):
    """Method: Integration
    Purpose: a task can be completed.
    Expected: 200 and done is True.
    """
    task_id = add_task(client).get_json()["id"]
    res = client.post(f"/api/tasks/{task_id}/complete")
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_us9_ac2_complete_unknown_task_returns_404(client):
    """Method: Integration
    Purpose: unknown id is handled.
    Expected: 404 with error message.
    """
    res = client.post("/api/tasks/999/complete")
    assert res.status_code == 404
    assert res.get_json()["error"] == "Task not found"


# US10 - Delete a task
def test_us10_ac1_delete_removes_task(client):
    """Method: Integration
    Purpose: a task can be deleted.
    Expected: 204 and list is empty.
    """
    task_id = add_task(client).get_json()["id"]
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get("/api/tasks").get_json() == []


def test_us10_ac2_delete_unknown_task_returns_404(client):
    """Method: Integration
    Purpose: deleting twice is handled.
    Expected: second delete gives 404.
    """
    task_id = add_task(client).get_json()["id"]
    client.delete(f"/api/tasks/{task_id}")
    assert client.delete(f"/api/tasks/{task_id}").status_code == 404
