# Secure Login System

A beginner-friendly secure login web application built with **Python, Flask, SQLite, SQLAlchemy, and bcrypt**.

The project demonstrates password hashing, input validation, protection against SQL injection through ORM queries, session-based authentication, and logout.

## Features

- User registration
- User login
- Password hashing using bcrypt
- Password verification using bcrypt
- Username and password validation
- SQLAlchemy ORM database queries
- SQLite database
- Session-based authentication
- Protected dashboard
- Logout feature
- Simple responsive web interface
- No plaintext passwords stored in the database

## Project Structure

```text
secure-login-system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
└── static/
    └── style.css
```

After the first run, Flask/SQLite will create a database file:

```text
instance/users.db
```

## Requirements

- Python 3.9 or newer
- pip

Install the dependencies:

```bash
pip install -r requirements.txt
```

On Windows:

```bash
py -m pip install -r requirements.txt
```

## Run the Application

Open the project folder in VS Code.

Then run:

```bash
python app.py
```

On Windows:

```bash
py app.py
```

The terminal will show a local address similar to:

```text
http://127.0.0.1:5000
```

Open that address in your browser.

## How It Works

### 1. Registration

The user provides:

- Username
- Password

The password is checked against basic requirements:

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

The password is then hashed with bcrypt before being stored.

The original plaintext password is not stored.

### 2. Login

During login, the application:

1. Finds the user by username.
2. Retrieves the stored bcrypt hash.
3. Uses bcrypt to verify the entered password.
4. Creates a session after successful authentication.

### 3. Session Management

After successful login:

```python
session["user_id"] = user.id
session["username"] = user.username
```

The dashboard uses a `login_required` decorator so that unauthenticated users cannot access it.

Logout clears the session:

```python
session.clear()
```

### 4. SQL Injection Protection

The project uses SQLAlchemy ORM instead of constructing SQL statements by concatenating user input.

For example:

```python
User.query.filter_by(username=username).first()
```

This helps avoid common SQL injection problems associated with unsafe SQL string construction.

## Security Concepts Demonstrated

### Password Hashing

Passwords are processed with bcrypt:

```python
bcrypt.generate_password_hash(password)
```

Verification uses:

```python
bcrypt.check_password_hash(stored_hash, password)
```

The application does not store the user's actual password.

### Input Validation

Usernames are restricted to:

```text
A-Z
a-z
0-9
_
```

and must be between 3 and 50 characters.

Passwords have basic complexity requirements.

### Session Security

The project enables:

- `HttpOnly` session cookies
- `SameSite=Lax`
- Session clearing on login/logout

For production applications, HTTPS and additional cookie settings such as `Secure` should be enabled.

## Optional 2FA

Two-factor authentication is not included in this beginner version.

A production implementation could add TOTP-based 2FA using an authenticator application.

## Important Production Security Improvements

This project is designed for learning. Before using a login system in production, add:

- HTTPS
- A strong random `SECRET_KEY` stored in environment variables
- Secure cookies
- CSRF protection
- Rate limiting / login throttling
- Account lockout or abuse protection
- Email verification
- Password reset with secure tokens
- TOTP or WebAuthn-based MFA
- Security logging and monitoring
- Stronger password policies based on current security guidance
- Production WSGI server instead of Flask's development server

Also set:

```text
SESSION_COOKIE_SECURE=True
```

when serving the application over HTTPS.

## Testing

Try these cases:

### Registration

Create:

```text
Username: vishalini
Password: Hello@123
```

Then log in with the same credentials.

### Invalid Password

Try:

```text
hello
```

The application should reject it because it does not satisfy the minimum requirements.

### Duplicate Username

Register the same username twice.

The application should display:

```text
Username already exists.
```

### Logout

After login, click **Logout** and try opening `/dashboard`.

The application should redirect you to the login page.

## GitHub Upload

After testing:

```bash
git init
git add .
git commit -m "Add secure login system"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your GitHub repository URL.

### Important

Do not upload real production secrets or real user databases to GitHub.

If you change the secret key, keep it in an environment variable rather than committing it to the repository.

## Internship / Submission Explanation

You can explain the project like this:

> "I developed a secure login web application using Python Flask. The application supports user registration and login with bcrypt password hashing, validates user input, uses SQLAlchemy ORM to reduce SQL injection risks, manages authenticated sessions, and provides a logout function. I also implemented a protected dashboard that can only be accessed after successful authentication."

## Learning Outcomes

This project helps demonstrate:

- Web authentication
- Password hashing
- bcrypt
- Flask sessions
- Input validation
- SQL injection awareness
- ORM-based database access
- Access control
- Logout/session management
- Basic secure coding practices

## Disclaimer

This is an educational project. It is not intended to be deployed directly as a production authentication service without additional security controls and professional security review.
