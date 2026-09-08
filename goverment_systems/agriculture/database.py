import sqlite3

DB_NAME = "agriculture.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)

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


def verify_land(citizen_id):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE subsidy_applications
        SET land_verified = 1,
            status = 'Verified'
        WHERE citizen_id = ?
    """, (citizen_id,))

    conn.commit()

    cursor.execute("""
        SELECT citizen_id, land_verified, status
        FROM subsidy_applications
        WHERE citizen_id = ?
    """, (citizen_id,))

    result = cursor.fetchone()

    conn.close()

    return result