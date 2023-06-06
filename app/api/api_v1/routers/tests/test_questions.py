from app.db.questions.models import Question


def test_question_crud(
    client, test_dimension, test_db, superuser_token_headers
):
    # Test create question object
    question = {
        "name": "TestQuestion",
        "description": "desc",
        "dimension_id": test_dimension.id,
    }
    response = client.post(
        "/api/v1/questions",
        json=question,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == question[arg] for arg in question)

    # Test get all question object
    response = client.get("/api/v1/questions", headers=superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == question["name"]

    # Edit question object
    question_id = response.json()[0]["id"]
    edit_question = {
        "name": "Updated Question",
        "description": "Updated Question",
        "dimension_id": test_dimension.id,
    }
    response = client.put(
        f"/api/v1/questions/{question_id}",
        json=edit_question,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(
        response.json()[arg] == edit_question[arg] for arg in edit_question
    )

    # Delete question object
    response = client.delete(
        f"/api/v1/questions/{question_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Question).all() == []
