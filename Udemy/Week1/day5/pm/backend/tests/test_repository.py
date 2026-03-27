from pathlib import Path

from app.kanban_repository import KanbanRepository


def test_database_bootstraps_on_initialize(tmp_path: Path) -> None:
    db_path = tmp_path / "bootstrap.db"
    repo = KanbanRepository(db_path)

    assert not db_path.exists()
    repo.initialize()

    assert db_path.exists()


def test_repository_crud_and_move_flow(tmp_path: Path) -> None:
    repo = KanbanRepository(tmp_path / "repo-flow.db")
    repo.initialize()

    board = repo.get_board("user")
    assert len(board["columns"]) == 5

    board = repo.rename_column("user", "col-backlog", "Ideas")
    assert board["columns"][0]["title"] == "Ideas"

    board = repo.create_card("user", "col-backlog", "card-test", "New Task", "Draft details")
    assert "card-test" in board["cards"]
    assert board["cards"]["card-test"]["title"] == "New Task"

    board = repo.update_card("user", "card-test", "Renamed Task", "Updated details")
    assert board["cards"]["card-test"]["title"] == "Renamed Task"

    board = repo.move_card("user", "card-test", "col-review", 0)
    review_col = next(column for column in board["columns"] if column["id"] == "col-review")
    assert review_col["cardIds"][0] == "card-test"

    board = repo.delete_card("user", "card-test")
    assert "card-test" not in board["cards"]


def test_data_persists_when_reopening_repository(tmp_path: Path) -> None:
    db_path = tmp_path / "persist.db"

    repo = KanbanRepository(db_path)
    repo.initialize()
    repo.create_card("user", "col-backlog", "card-persist", "Persist me", "Keep after restart")

    reopened_repo = KanbanRepository(db_path)
    reopened_repo.initialize()
    board = reopened_repo.get_board("user")

    assert "card-persist" in board["cards"]
