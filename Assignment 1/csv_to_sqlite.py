
import csv
import sqlite3

CSV_FILE = "users.csv"
DB_NAME = "users.db"


def import_users():
    inserted = 0
    skipped = 0

    with open(CSV_FILE, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not {"name", "email"}.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV must contain name and email columns.")

        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)

            for row in reader:
                name = (row.get("name") or "").strip()
                email = (row.get("email") or "").strip()

                if not name or not email:
                    skipped += 1
                    continue

                cursor = conn.execute("""
                    INSERT OR IGNORE INTO users (name, email)
                    VALUES (?, ?)
                """, (name, email))

                if cursor.rowcount == 1:
                    inserted += 1
                else:
                    skipped += 1

            rows = conn.execute("""
                SELECT id, name, email
                FROM users
                ORDER BY id
            """).fetchall()

    print(f"New users inserted: {inserted}")
    print(f"Rows skipped: {skipped}")
    print("\nUsers in the database:")

    for user_id, name, email in rows:
        print(f"{user_id}. {name} - {email}")


if __name__ == "__main__":
    try:
        import_users()
    except (OSError, csv.Error, sqlite3.Error, ValueError) as error:
        print(f"Import failed: {error}")