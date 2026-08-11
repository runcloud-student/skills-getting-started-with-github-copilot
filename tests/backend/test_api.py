from urllib.parse import quote


def test_get_activities_returns_the_activity_catalog(client):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Music Ensemble",
        "Debate Team",
        "Science Olympiad",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_names


def test_signup_for_activity_adds_the_student_when_the_email_is_new(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@example.com"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_for_activity_rejects_a_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(duplicate_email, safe='')}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_the_email_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    signup_response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"
    )

    # Act
    unregister_response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_participant_returns_not_found_for_a_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_for_activity_returns_not_found_for_an_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
