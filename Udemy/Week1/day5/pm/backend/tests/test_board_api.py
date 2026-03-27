from pathlib import Path

from fastapi.testclient import TestClient

from app.kanban_repository import KanbanRepository
from app.main import app


def make_client(db_path: Path) -> TestClient:
    app.state.repo = KanbanRepository(db_path)
    app.state.repo.initialize()
    return TestClient(app)


def test_get_board_returns_seeded_state(tmp_path: Path) -> None:
    with make_client(tmp_path / "board.db") as client:
        response = client.get("/api/board")

    assert response.status_code == 200
    payload = response.json()
    assert payload["user"] == "user"
    assert len(payload["columns"]) == 5
    assert "card-1" in payload["cards"]


def test_full_card_lifecycle_and_column_rename(tmp_path: Path) -> None:
    with make_client(tmp_path / "flow.db") as client:
        rename_response = client.patch(
            "/api/columns/col-backlog",
            json={"user": "user", "title": "Ideas"},
        )
        assert rename_response.status_code == 200
        assert rename_response.json()["columns"][0]["title"] == "Ideas"

        create_response = client.post(
            "/api/cards",
            json={
                "user": "user",
                "columnId": "col-backlog",
                "title": "API Card",
                "details": "Created from integration test",
            },
        )
        assert create_response.status_code == 200
        created_board = create_response.json()
        created_card_id = next(
            card_id
            for card_id, card in created_board["cards"].items()
            if card["title"] == "API Card"
        )

        update_response = client.patch(
            f"/api/cards/{created_card_id}",
            json={"user": "user", "title": "API Card Updated"},
        )
        assert update_response.status_code == 200
        assert (
            update_response.json()["cards"][created_card_id]["title"]
            == "API Card Updated"
        )

        move_response = client.post(
            f"/api/cards/{created_card_id}/move",
            json={"user": "user", "toColumnId": "col-review", "toIndex": 0},
        )
        assert move_response.status_code == 200
        review_column = next(
            column
            for column in move_response.json()["columns"]
            if column["id"] == "col-review"
        )
        assert review_column["cardIds"][0] == created_card_id

        delete_response = client.delete(f"/api/cards/{created_card_id}")
        assert delete_response.status_code == 200
        assert created_card_id not in delete_response.json()["cards"]


def test_error_contract_for_invalid_operation(tmp_path: Path) -> None:
    with make_client(tmp_path / "errors.db") as client:
        response = client.patch(
            "/api/columns/col-unknown",
            json={"user": "user", "title": "Nope"},
        )

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "not_found"
    assert "message" in payload["error"]


def test_bootstrap_happens_on_first_api_call(tmp_path: Path) -> None:
    db_path = tmp_path / "first-run.db"
    assert not db_path.exists()

    app.state.repo = KanbanRepository(db_path)
    with TestClient(app) as client:
        response = client.get("/api/board")

    assert response.status_code == 200
    assert db_path.exists()


def test_persistence_across_clients_with_same_db(tmp_path: Path) -> None:
    db_path = tmp_path / "persist-api.db"

    with make_client(db_path) as first_client:
        create_response = first_client.post(
            "/api/cards",
            json={
                "user": "user",
                "columnId": "col-backlog",
                "title": "Persisted API Card",
                "details": "Should still exist",
            },
        )
        assert create_response.status_code == 200

    with make_client(db_path) as second_client:
        board_response = second_client.get("/api/board")
        assert board_response.status_code == 200

    titles = [card["title"] for card in board_response.json()["cards"].values()]
    assert "Persisted API Card" in titles
