from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pm.db"

DEFAULT_COLUMNS: list[tuple[str, str]] = [
    ("col-backlog", "Backlog"),
    ("col-discovery", "Discovery"),
    ("col-progress", "In Progress"),
    ("col-review", "Review"),
    ("col-done", "Done"),
]

DEFAULT_CARDS: list[tuple[str, str, str, str]] = [
    (
        "card-1",
        "col-backlog",
        "Align roadmap themes",
        "Draft quarterly themes with impact statements and metrics.",
    ),
    (
        "card-2",
        "col-backlog",
        "Gather customer signals",
        "Review support tags, sales notes, and churn feedback.",
    ),
    (
        "card-3",
        "col-discovery",
        "Prototype analytics view",
        "Sketch initial dashboard layout and key drill-downs.",
    ),
    (
        "card-4",
        "col-progress",
        "Refine status language",
        "Standardize column labels and tone across the board.",
    ),
    (
        "card-5",
        "col-progress",
        "Design card layout",
        "Add hierarchy and spacing for scanning dense lists.",
    ),
    (
        "card-6",
        "col-review",
        "QA micro-interactions",
        "Verify hover, focus, and loading states.",
    ),
    (
        "card-7",
        "col-done",
        "Ship marketing page",
        "Final copy approved and asset pack delivered.",
    ),
    (
        "card-8",
        "col-done",
        "Close onboarding sprint",
        "Document release notes and share internally.",
    ),
]


@dataclass
class RepositoryError(Exception):
    status_code: int
    code: str
    message: str
    details: dict[str, Any] | None = None


class KanbanRepository:
    def __init__(self, db_path: Path | str | None = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE
                );

                CREATE TABLE IF NOT EXISTS boards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS columns (
                    id TEXT PRIMARY KEY,
                    board_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS cards (
                    id TEXT PRIMARY KEY,
                    board_id INTEGER NOT NULL,
                    column_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    details TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
                    FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_columns_board_position
                    ON columns (board_id, position);
                CREATE INDEX IF NOT EXISTS idx_cards_board_column_position
                    ON cards (board_id, column_id, position);
                """
            )
            self._ensure_board(conn, "user")

    def get_board(self, username: str) -> dict[str, Any]:
        with self._connect() as conn:
            board_id = self._ensure_board(conn, username)
            return self._read_board(conn, username, board_id)

    def rename_column(self, username: str, column_id: str, title: str) -> dict[str, Any]:
        normalized = title.strip()
        if not normalized:
            raise RepositoryError(400, "validation_error", "Column title cannot be empty")

        with self._connect() as conn:
            board_id = self._ensure_board(conn, username)
            updated = conn.execute(
                """
                UPDATE columns
                SET title = ?
                WHERE id = ? AND board_id = ?
                """,
                (normalized, column_id, board_id),
            ).rowcount
            if updated == 0:
                raise RepositoryError(404, "not_found", "Column not found", {"columnId": column_id})
            return self._read_board(conn, username, board_id)

    def create_card(self, username: str, column_id: str, card_id: str, title: str, details: str) -> dict[str, Any]:
        normalized_title = title.strip()
        normalized_details = details.strip() or "No details yet."
        if not normalized_title:
            raise RepositoryError(400, "validation_error", "Card title cannot be empty")

        with self._connect() as conn:
            board_id = self._ensure_board(conn, username)
            self._ensure_column_exists(conn, board_id, column_id)
            next_position = self._next_card_position(conn, board_id, column_id)
            conn.execute(
                """
                INSERT INTO cards (id, board_id, column_id, title, details, position)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (card_id, board_id, column_id, normalized_title, normalized_details, next_position),
            )
            return self._read_board(conn, username, board_id)

    def update_card(
        self,
        username: str,
        card_id: str,
        title: str | None,
        details: str | None,
    ) -> dict[str, Any]:
        if title is None and details is None:
            raise RepositoryError(
                400,
                "validation_error",
                "Provide at least one field to update",
            )

        with self._connect() as conn:
            board_id = self._ensure_board(conn, username)
            row = conn.execute(
                """
                SELECT title, details
                FROM cards
                WHERE id = ? AND board_id = ?
                """,
                (card_id, board_id),
            ).fetchone()
            if row is None:
                raise RepositoryError(404, "not_found", "Card not found", {"cardId": card_id})

            next_title = title.strip() if title is not None else row["title"]
            next_details = details.strip() if details is not None else row["details"]
            if not next_title:
                raise RepositoryError(400, "validation_error", "Card title cannot be empty")

            conn.execute(
                """
                UPDATE cards
                SET title = ?, details = ?
                WHERE id = ? AND board_id = ?
                """,
                (next_title, next_details, card_id, board_id),
            )
            return self._read_board(conn, username, board_id)

    def move_card(
        self,
        username: str,
        card_id: str,
        to_column_id: str,
        to_index: int,
    ) -> dict[str, Any]:
        if to_index < 0:
            raise RepositoryError(400, "validation_error", "toIndex must be >= 0")

        with self._connect() as conn:
            board_id = self._ensure_board(conn, username)
            card_row = conn.execute(
                """
                SELECT id, column_id, position
                FROM cards
                WHERE id = ? AND board_id = ?
                """,
                (card_id, board_id),
            ).fetchone()
            if card_row is None:
                raise RepositoryError(404, "not_found", "Card not found", {"cardId": card_id})

            self._ensure_column_exists(conn, board_id, to_column_id)

            from_column_id = card_row["column_id"]
            from_index = int(card_row["position"])

            conn.execute(
                """
                UPDATE cards
                SET position = position - 1
                WHERE board_id = ? AND column_id = ? AND position > ?
                """,
                (board_id, from_column_id, from_index),
            )

            adjusted_index = to_index
            if from_column_id == to_column_id and to_index > from_index:
                adjusted_index -= 1

            max_position_row = conn.execute(
                """
                SELECT COALESCE(MAX(position), -1) AS max_position
                FROM cards
                WHERE board_id = ? AND column_id = ?
                """,
                (board_id, to_column_id),
            ).fetchone()
            max_position = int(max_position_row["max_position"])
            bounded_index = min(max(adjusted_index, 0), max_position + 1)

            conn.execute(
                """
                UPDATE cards
                SET position = position + 1
                WHERE board_id = ? AND column_id = ? AND position >= ?
                """,
                (board_id, to_column_id, bounded_index),
            )

            conn.execute(
                """
                UPDATE cards
                SET column_id = ?, position = ?
                WHERE id = ? AND board_id = ?
                """,
                (to_column_id, bounded_index, card_id, board_id),
            )
            return self._read_board(conn, username, board_id)

    def delete_card(self, username: str, card_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            board_id = self._ensure_board(conn, username)
            card_row = conn.execute(
                """
                SELECT column_id, position
                FROM cards
                WHERE id = ? AND board_id = ?
                """,
                (card_id, board_id),
            ).fetchone()
            if card_row is None:
                raise RepositoryError(404, "not_found", "Card not found", {"cardId": card_id})

            conn.execute(
                """
                DELETE FROM cards
                WHERE id = ? AND board_id = ?
                """,
                (card_id, board_id),
            )
            conn.execute(
                """
                UPDATE cards
                SET position = position - 1
                WHERE board_id = ? AND column_id = ? AND position > ?
                """,
                (board_id, card_row["column_id"], int(card_row["position"])),
            )
            return self._read_board(conn, username, board_id)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _ensure_board(self, conn: sqlite3.Connection, username: str) -> int:
        normalized_user = username.strip().lower()
        if not normalized_user:
            raise RepositoryError(400, "validation_error", "Username cannot be empty")

        conn.execute(
            """
            INSERT INTO users (username)
            VALUES (?)
            ON CONFLICT(username) DO NOTHING
            """,
            (normalized_user,),
        )
        user_row = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            (normalized_user,),
        ).fetchone()
        assert user_row is not None
        user_id = int(user_row["id"])

        board_row = conn.execute(
            "SELECT id FROM boards WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if board_row is not None:
            return int(board_row["id"])

        board_cursor = conn.execute(
            "INSERT INTO boards (user_id, name) VALUES (?, ?)",
            (user_id, "Main Board"),
        )
        board_id = int(board_cursor.lastrowid)

        for index, (column_id, title) in enumerate(DEFAULT_COLUMNS):
            conn.execute(
                """
                INSERT INTO columns (id, board_id, title, position)
                VALUES (?, ?, ?, ?)
                """,
                (column_id, board_id, title, index),
            )

        for card_id, column_id, title, details in DEFAULT_CARDS:
            position = self._next_card_position(conn, board_id, column_id)
            conn.execute(
                """
                INSERT INTO cards (id, board_id, column_id, title, details, position)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (card_id, board_id, column_id, title, details, position),
            )

        return board_id

    def _next_card_position(self, conn: sqlite3.Connection, board_id: int, column_id: str) -> int:
        row = conn.execute(
            """
            SELECT COALESCE(MAX(position), -1) AS max_position
            FROM cards
            WHERE board_id = ? AND column_id = ?
            """,
            (board_id, column_id),
        ).fetchone()
        return int(row["max_position"]) + 1

    def _ensure_column_exists(self, conn: sqlite3.Connection, board_id: int, column_id: str) -> None:
        row = conn.execute(
            """
            SELECT id
            FROM columns
            WHERE id = ? AND board_id = ?
            """,
            (column_id, board_id),
        ).fetchone()
        if row is None:
            raise RepositoryError(404, "not_found", "Column not found", {"columnId": column_id})

    def _read_board(self, conn: sqlite3.Connection, username: str, board_id: int) -> dict[str, Any]:
        columns_rows = conn.execute(
            """
            SELECT id, title
            FROM columns
            WHERE board_id = ?
            ORDER BY position ASC
            """,
            (board_id,),
        ).fetchall()

        cards_rows = conn.execute(
            """
            SELECT id, column_id, title, details
            FROM cards
            WHERE board_id = ?
            ORDER BY column_id ASC, position ASC
            """,
            (board_id,),
        ).fetchall()

        cards: dict[str, dict[str, str]] = {}
        card_ids_by_column: dict[str, list[str]] = {row["id"]: [] for row in columns_rows}

        for row in cards_rows:
            card_id = row["id"]
            cards[card_id] = {
                "id": card_id,
                "title": row["title"],
                "details": row["details"],
            }
            card_ids_by_column[row["column_id"]].append(card_id)

        columns = [
            {
                "id": row["id"],
                "title": row["title"],
                "cardIds": card_ids_by_column[row["id"]],
            }
            for row in columns_rows
        ]

        return {
            "user": username.strip().lower(),
            "columns": columns,
            "cards": cards,
        }
