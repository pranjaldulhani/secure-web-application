from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import html
import logging

app = Flask(__name__)

# Security monitoring / logging
logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Database connection
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # 1. Input validation and sanitization
        name = html.escape(request.form.get("name", "").strip())
        email = html.escape(request.form.get("email", "").strip())
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            logging.warning("Invalid/empty input received")
            return "All fields are required!"

        if "@" not in email:
            logging.warning("Invalid email entered")
            return "Please enter a valid email!"

        # 2. Prepared statement to prevent SQL Injection
        conn = get_db()

        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        logging.info("New user registered successfully")

        return redirect(url_for("success"))

    return render_template("index.html")


@app.route("/success")
def success():
    return """
    <h2>Registration Successful!</h2>
    <p>Your data was securely processed.</p>
    <a href="/">Go Back</a>
    """


# 5. Security headers
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "no-referrer"

    return response


if __name__ == "__main__":
    init_db()

    # 4. HTTPS for secure data transmission
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000,
        ssl_context="adhoc"
    )