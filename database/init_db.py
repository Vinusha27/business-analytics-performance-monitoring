from __future__ import annotations
import sqlite3
from config import DB_PATH

def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript((__import__('pathlib').Path(__file__).with_name('schema.sql')).read_text())

if __name__ == '__main__': initialize_database()
