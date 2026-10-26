from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "library-management-local-key"
DB_PATH = Path(__file__).with_name("library.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        if not title or not author:
            flash("Please enter both the book title and author.", "error")
        else:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO books (title, author) VALUES (?, ?)",
                    (title, author)
                )
            flash("Book added successfully.", "success")
        return redirect(url_for("index"))

    search = request.args.get("search", "").strip()
    with get_db() as conn:
        if search:
            books = conn.execute(
                "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC",
                (f"%{search}%", f"%{search}%")
            ).fetchall()
        else:
            books = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()

    return render_template("index.html", books=books, search=search)


@app.post("/delete/<int:book_id>")
def delete_book(book_id):
    with get_db() as conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    flash("Book deleted.", "success")
    return redirect(url_for("index"))


@app.post("/toggle/<int:book_id>")
def toggle_book(book_id):
    with get_db() as conn:
        book = conn.execute("SELECT available FROM books WHERE id = ?", (book_id,)).fetchone()
        if book is not None:
            new_status = 0 if book["available"] else 1
            conn.execute("UPDATE books SET available = ? WHERE id = ?", (new_status, book_id))
            flash("Book issued." if new_status == 0 else "Book returned.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
