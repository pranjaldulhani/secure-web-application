# Secure Web Application

## Objective

The objective of this project is to implement security best practices in a simple web application and protect user data from common web security threats.

## Security Features

This application implements the following security features:

1. **Input Validation**
   - Validates name, email, and password.
   - Checks required fields and input length.

2. **SQL Injection Prevention**
   - Uses prepared statements with parameterized queries.
   - Prevents malicious SQL commands from being executed.

3. **XSS Protection**
   - Uses Flask/Jinja2 template auto-escaping.
   - User input is not directly rendered as HTML.

4. **Password Hashing**
   - Passwords are never stored in plain text.
   - Passwords are securely hashed before storing them in the database.

5. **HTTPS**
   - The application supports HTTPS for secure communication.
   - Local testing uses a self-signed certificate.

6. **Security Headers**
   - X-Content-Type-Options
   - X-Frame-Options
   - Content-Security-Policy
   - Referrer-Policy

7. **Security Monitoring and Logging**
   - Records security-related events such as registration failures and duplicate email attempts.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS

## Project Structure

```text
secure-web-application/
│
├── app.py
├── .gitignore
└── templates/
    └── index.html
