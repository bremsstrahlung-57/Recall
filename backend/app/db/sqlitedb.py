import os
import sqlite3
from datetime import datetime

from app.core.constants import DATA_FILE_PATH, DATA_PATH


def make_cache_folder():
    """Create cache/ folder if doesn't exists already"""
    try:
        os.mkdir(DATA_PATH)
        return f"Folder '{DATA_PATH}' created successfully."
    except FileExistsError:
        return f"Folder '{DATA_PATH}' already exists."
    except FileNotFoundError:
        return "Parent directory does not exist."


class SQLiteDB:
    """All functions related to SQLite Database storing user docs and all other important metadata"""

    def __init__(self) -> None:
        self.connection = sqlite3.connect(DATA_FILE_PATH, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.now = datetime.now()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        title TEXT,
        content TEXT NOT NULL,
        source TEXT,
        total_chunks INTEGER,
        created_at TEXT
        );""")

    def insert_doc_ib_db(
        self, doc_id: str, title: str, content: str, source: str, total_chunks: int
    ) -> None:
        """Save full doc and other metadata in the SQLite DB"""
        make_cache_folder()
        _doc_id = doc_id
        iso_format = self.now.strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute(
            """
        INSERT OR REPLACE INTO documents (doc_id, title, content, source, total_chunks, created_at)
        VALUES(?, ?, ?, ?, ?, ?)
        """,
            (doc_id, title, content, source, total_chunks, iso_format),
        )

        self.connection.commit()

    def read_from_cache(self) -> list:
        """Get all the rows from SQLite DB"""
        self.cursor.execute("SELECT * FROM documents")
        rows = self.cursor.fetchall()

        return rows
