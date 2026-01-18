from datetime import datetime
import os
import sqlite3
from app.core.constants import CACHE_PATH, CACHE_FILE_PATH


def make_cache_folder():
    """Create cache/ folder if doesn't exists already"""
    try:
        os.mkdir(CACHE_PATH)
        return f"Folder '{CACHE_PATH}' created successfully."
    except FileExistsError:
        return f"Folder '{CACHE_PATH}' already exists."
    except FileNotFoundError:
        return "Parent directory does not exist."


class SQLiteDB:
    """All functions related to SQLite Database storing user docs and all other important metadata"""
    def __init__(self) -> None:
        self.connection = sqlite3.connect(CACHE_FILE_PATH)
        self.cursor = self.connection.cursor()
        self.now = datetime.now()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        source TEXT,
        total_chunks INTEGER,
        created_at TEXT
        );""")

    def insert_doc_ib_db(self, doc_id:str, content:str, source: str, total_chunks:int) -> None:
        """Save full doc and other metadata in the SQLite DB"""
        make_cache_folder()
        _doc_id = doc_id
        iso_format = self.now.strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
        INSERT OR REPLACE INTO documents (doc_id, content, source, total_chunks, created_at)
        VALUES(?, ?, ?, ?, ?)
        """, (doc_id, content, source, total_chunks, iso_format))

        self.connection.commit()

    def read_from_cache(self) -> list:
        """Get all the rows from SQLite DB"""
        self.cursor.execute("SELECT * FROM documents")
        rows = self.cursor.fetchall()

        return rows
    