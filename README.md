# Library Management System

A small library management website built with Python Flask, HTML, CSS, and SQLite.

## Features
- Add books
- Search by book title or author
- View all books
- Issue a book
- Return a book
- Delete a book
- Automatically creates the SQLite database

## Requirements
- Python 3.9 or newer
- Flask

## Run on Windows

1. Extract the ZIP file.
2. Open the extracted `library_management` folder in VS Code.
3. Open a terminal in that folder.
4. Install Flask:

   ```bash
   python -m pip install flask
   ```

5. Start the website:

   ```bash
   python app.py
   ```

6. Open this address in your browser:

   http://127.0.0.1:5000

The `library.db` database file is created automatically the first time the app runs.

To stop the server, press `Ctrl+C` in the terminal.
