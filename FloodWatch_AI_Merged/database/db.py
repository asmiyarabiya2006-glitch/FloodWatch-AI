import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "floodwatch.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS flood_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT,
                rainfall REAL,
                water_level REAL,
                flood_risk TEXT,
                model_target TEXT,
                input_json TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        existing = {row["name"] for row in connection.execute("PRAGMA table_info(flood_data)")}
        additions = {
            "location": "TEXT",
            "model_target": "TEXT",
            "input_json": "TEXT",
        }
        for name, kind in additions.items():
            if name not in existing:
                connection.execute(f"ALTER TABLE flood_data ADD COLUMN {name} {kind}")
        connection.commit()
    finally:
        connection.close()
