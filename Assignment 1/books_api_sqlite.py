
import sqlite3
import requests

API_URL = "https://openlibrary.org/search.json?q=python&limit=20"
DB_NAME = "books.db"


def fetch_books():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()

    books = []
    for item in data.get("docs", []):
        title = item.get("title")
        if not title:
            continue

        authors = item.get("author_name", [])
        author = ", ".join(authors) if authors else None

        years = item.get("first_publish_year")
        books.append((title, author, years))

    return books


def store_books(books):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                publication_year INTEGER
            )
        """)

        conn.executemany("""
            INSERT INTO books (title, author, publication_year)
            VALUES (?, ?, ?)
        """, books)


def display_books():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT title, author, publication_year
            FROM books
            ORDER BY title
        """).fetchall()

    print("\nBooks stored in the database:")
    for title, author, year in rows:
        print(f"Title: {title}")
        print(f"Author: {author or 'Unknown'}")
        print(f"Publication year: {year or 'Unknown'}")
        print("-" * 40)


def main():
    try:
        books = fetch_books()

        if not books:
            print("No books were returned by the API.")
            return

        store_books(books)
        print(f"Retrieved and stored {len(books)} books.")
        display_books()

    except requests.RequestException as error:
        print(f"API request failed: {error}")
    except sqlite3.Error as error:
        print(f"Database operation failed: {error}")


if __name__ == "__main__":
    main()