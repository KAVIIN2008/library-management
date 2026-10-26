# Library Management Dashboard

A polished library management website built with Python Flask, HTML, CSS, and SQLite.

## Features
- Add books
- Search by book title or author
- View all books
- Issue a book
- Return a book
- Delete a book
- Collection summary cards for total, available, and issued books
- Responsive layout with accessible labels, focus states, and empty states
- Server-side validation for book details
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
It is intentionally ignored by Git because it contains local application data.

## Configuration

For a non-local deployment, set a strong secret key before starting the app:

```powershell
$env:LIBRARY_SECRET_KEY = "replace-with-a-long-random-value"
$env:FLASK_DEBUG = "false"
python app.py
```

To stop the server, press `Ctrl+C` in the terminal.

## Deploy publicly with Render

The repository includes a [`render.yaml`](./render.yaml) blueprint for deployment:

1. Sign in to [Render](https://render.com/) with GitHub.
2. Select **New > Blueprint**.
3. Choose `KAVIIN2008/library-management`.
4. Confirm the `library-management` web service and select **Apply**.
5. Wait for the build to finish, then open the generated `.onrender.com` URL.

The Render free tier uses an ephemeral filesystem. Because this app stores books in
SQLite, its data can be lost when the service is redeployed or restarted. For
reliable long-term data, use a persistent disk or migrate the database to a hosted
PostgreSQL service before production use.
