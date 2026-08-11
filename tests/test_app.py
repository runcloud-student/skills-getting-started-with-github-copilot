from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities


def test_unregister_participant_removes_the_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    signup_response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
