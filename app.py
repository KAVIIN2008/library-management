import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "LIBRARY_SECRET_KEY", "library-management-local-development-key"
)
DB_PATH = Path(__file__).with_name("library.db")
MAX_FIELD_LENGTH = 120
MAX_SEARCH_LENGTH = 100


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1
            )
        """)


init_db()


def get_library_stats() -> dict[str, int]:
    with get_db() as conn:
        stats = conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(available), 0) AS available,
                COALESCE(SUM(CASE WHEN available = 0 THEN 1 ELSE 0 END), 0) AS issued
            FROM books
            """
        ).fetchone()
    return dict(stats)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        errors = []
        if not title:
            errors.append("Enter a book title.")
        if not author:
            errors.append("Enter an author name.")
        if len(title) > MAX_FIELD_LENGTH or len(author) > MAX_FIELD_LENGTH:
            errors.append(f"Titles and author names must be {MAX_FIELD_LENGTH} characters or fewer.")

        if errors:
            flash(" ".join(errors), "error")
        else:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO books (title, author) VALUES (?, ?)",
                    (title, author)
                )
            flash("Book added successfully.", "success")
        return redirect(url_for("index"))

    search = request.args.get("search", "").strip()[:MAX_SEARCH_LENGTH]
    with get_db() as conn:
        if search:
            books = conn.execute(
                "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC",
                (f"%{search}%", f"%{search}%")
            ).fetchall()
        else:
            books = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()

    return render_template(
        "index.html",
        books=books,
        search=search,
        stats=get_library_stats(),
        max_field_length=MAX_FIELD_LENGTH,
    )


@app.post("/delete/<int:book_id>")
def delete_book(book_id):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    if cursor.rowcount:
        flash("Book deleted.", "success")
    else:
        flash("That book could not be found.", "error")
    return redirect(url_for("index"))


@app.post("/toggle/<int:book_id>")
def toggle_book(book_id):
    with get_db() as conn:
        book = conn.execute("SELECT available FROM books WHERE id = ?", (book_id,)).fetchone()
        if book is not None:
            new_status = 0 if book["available"] else 1
            conn.execute("UPDATE books SET available = ? WHERE id = ?", (new_status, book_id))
            flash("Book issued." if new_status == 0 else "Book returned.", "success")
        else:
            flash("That book could not be found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=os.environ.get("FLASK_DEBUG", "").lower() == "true")
