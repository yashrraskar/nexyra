import sqlite3

DB_NAME = "revenue.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
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


def get_land_record(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT citizen_id, citizen_name, land_id, area, verified
        FROM land_records
        WHERE citizen_id = ?
    """, (citizen_id,))

    result = cursor.fetchone()

    conn.close()

    return result