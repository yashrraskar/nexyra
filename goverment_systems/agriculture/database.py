import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "agriculture.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subsidy_applications (
            application_id TEXT PRIMARY KEY,
            citizen_id TEXT,
            subsidy_type TEXT,
            land_verified BOOLEAN,
            status TEXT
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO subsidy_applications
        VALUES ('A001', 'C001', 'Agriculture Subsidy', 0, 'Pending')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO subsidy_applications
        VALUES ('A002', 'C002', 'Agriculture Subsidy', 0, 'Pending')
    """)

    conn.commit()
    conn.close()


def reset_database():
    """Resets applications to original initial pending state for demo testing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS subsidy_applications")
    conn.commit()
    conn.close()
    create_database()


def verify_land(citizen_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if application exists
    cursor.execute("""
        SELECT application_id FROM subsidy_applications WHERE citizen_id = ?
    """, (citizen_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    cursor.execute("""
        UPDATE subsidy_applications
        SET land_verified = 1,
            status = 'Verified'
        WHERE citizen_id = ?
    """, (citizen_id,))

    conn.commit()

    cursor.execute("""
        SELECT citizen_id, land_verified, status, application_id, subsidy_type
        FROM subsidy_applications
        WHERE citizen_id = ?
    """, (citizen_id,))

    result = cursor.fetchone()
    conn.close()
    return result


def get_application(application_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT application_id, citizen_id, subsidy_type, land_verified, status
        FROM subsidy_applications
        WHERE application_id = ?
    """, (application_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_application_by_citizen(citizen_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT application_id, citizen_id, subsidy_type, land_verified, status
        FROM subsidy_applications
        WHERE citizen_id = ?
    """, (citizen_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_all_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT application_id, citizen_id, subsidy_type, land_verified, status
        FROM subsidy_applications
        ORDER BY application_id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows