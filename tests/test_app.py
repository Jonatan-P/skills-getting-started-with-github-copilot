from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    email = "test.user@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup?email=test.user%40mergington.edu"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test.user@mergington.edu for Chess Club"

    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_signup_duplicate_returns_400():
    email = "duplicate.user@mergington.edu"
    first = client.post(
        "/activities/Gym%20Class/signup?email=duplicate.user%40mergington.edu"
    )
    assert first.status_code == 200

    second = client.post(
        "/activities/Gym%20Class/signup?email=duplicate.user%40mergington.edu"
    )
    assert second.status_code == 400
    assert second.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_unregisters_from_activity():
    email = "remove.user@mergington.edu"
    signup = client.post(
        "/activities/Programming%20Class/signup?email=remove.user%40mergington.edu"
    )
    assert signup.status_code == 200

    delete = client.delete(
        "/activities/Programming%20Class/participants?email=remove.user%40mergington.edu"
    )
    assert delete.status_code == 200
    assert delete.json()["message"] == "Removed remove.user@mergington.edu from Programming Class"

    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]
