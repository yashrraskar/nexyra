import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "revenue.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS land_records (
            citizen_id TEXT PRIMARY KEY,
            citizen_name TEXT,
            land_id TEXT,
            area REAL,
            verified BOOLEAN
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO land_records
        VALUES ('C001', 'Rahul', 'MH-LAND-101', 2.5, 1)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO land_records
        VALUES ('C002', 'Amit', 'MH-LAND-102', 4.0, 1)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO land_records
        VALUES ('C003', 'Priya', 'MH-LAND-103', 1.8, 0)
    """)

    conn.commit()
    conn.close()


def reset_database():
    """Resets seed records to original initial state for demo testing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS land_records")
    conn.commit()
    conn.close()
    create_database()


def get_land_record(citizen_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT citizen_id, citizen_name, land_id, area, verified
        FROM land_records
        WHERE citizen_id = ?
    """, (citizen_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def get_all_land_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT citizen_id, citizen_name, land_id, area, verified
        FROM land_records
        ORDER BY citizen_id ASC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows