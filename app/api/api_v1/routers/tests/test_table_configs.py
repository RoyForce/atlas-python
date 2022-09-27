from app.db.table_configs.models import TableConfig


def test_get_table_configs(client, test_table_config, superuser_token_headers):
    response = client.get(
        "/api/v1/table-configs", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_table_config.id,
            "user_id": test_table_config.user_id,
            "table": test_table_config.table,
            "config": test_table_config.config,
        }
    ]


def test_delete_table_config(
    client, test_table_config, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/table-configs/{test_table_config.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(TableConfig).all() == []


def test_edit_table_config(client, test_table_config, superuser_token_headers):
    new_table_config = {
        "user_id": 1,
        "table": "JOB_ROLE_MATRIX",
        "config": {"test": "test"},
    }

    response = client.put(
        f"/api/v1/table-configs/{test_table_config.id}",
        json=new_table_config,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_table_config["id"] = test_table_config.id
    assert response.json() == new_table_config
