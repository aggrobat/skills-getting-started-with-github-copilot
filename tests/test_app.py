from fastapi.testclient import TestClient
import pytest

from src import app as application

client = TestClient(application.app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity: activities dict contains an expected activity
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure clean start: remove if present
    if email in application.activities[activity]["participants"]:
        application.activities[activity]["participants"].remove(email)

    # Sign up should succeed
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in application.activities[activity]["participants"]

    # Duplicate sign-up should be rejected
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Remove the participant
    resp_remove = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_remove.status_code == 200
    assert email not in application.activities[activity]["participants"]

    # Removing again should return 404
    resp_remove_again = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_remove_again.status_code == 404
