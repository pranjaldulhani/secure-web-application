from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("users.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- SECURITY LOGGING ----------------

def write_log(message):
    with open("security.log", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} - {message}\n")


# ---------------- REGISTRATION ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Get form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Input validation
        if not name or not email or not password:
            write_log("Registration failed: missing fields")
            return "All fields are required."

        if len(name) > 50:
            write_log("Registration failed: name too long")
            return "Name is too long."

        if "@" not in email:
            write_log("Registration failed: invalid email")
            return "Invalid email address."

        if len(password) < 6:
            write_log("Registration failed: weak password")
            return "Password must contain at least 6 characters."

        # Password hashing
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect("users.db")

            # Prepared statement
            # Prevents SQL Injection
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()
            conn.close()

            # Security monitoring
            write_log(f"New user registered: {email}")

            return redirect(url_for("success"))

        except sqlite3.IntegrityError:

            # Security monitoring
            write_log(f"Duplicate email attempted: {email}")

            return "Email already registered."

    # Display registration form
    return render_template("index.html")


# ---------------- SUCCESS PAGE ----------------

@app.route("/success")
def success():

    return """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Registration Successful</title>
    </head>

    <body>

        <h1>Registration Successful!</h1>

        <p>Your data has been securely stored.</p>

        <a href="/">Go Back</a>

    </body>

    </html>
    """


# ---------------- SECURITY HEADERS ----------------

@app.after_request
def security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Content-Security-Policy"] = "default-src 'self'"

    response.headers["Referrer-Policy"] = "no-referrer"

    return response


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":

    init_db()

    print("STARTING SECURE WEB APPLICATION")

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=False,
        use_reloader=False,
        ssl_context="adhoc"
    )
