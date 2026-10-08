# Secure Web Application

## Project Overview

The Secure Web Application is a simple web-based registration system developed using Python and Flask.

The main purpose of this project is to implement important web security best practices and protect user data from common security threats.

## Objective

The objective of this project is to implement security best practices in a web application.

The project focuses on:

- Input Validation
- SQL Injection Prevention
- Cross-Site Scripting (XSS) Protection
- Password Hashing
- HTTPS
- Security Headers
- Security Monitoring and Logging

## Security Features

### 1. Input Validation

The application validates user input before processing it.

It checks:

- Required fields
- Name length
- Email format
- Minimum password length

### 2. SQL Injection Prevention

The application uses parameterized queries to prevent SQL Injection attacks.

Example:

```python
conn.execute(
    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
    (name, email, hashed_password)
)
