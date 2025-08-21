# Flask Authentication App

This is a Flask-based web application that provides user registration, login, email verification, password reset, and forgot password functionalities. It uses MySQL as the database, Flask-Mail for email verification, and Flask-WTF for form handling.

## Features

- User registration with email verification.
- User login.
- Password reset.
- Forgot password functionality.
- Simple gallery page accessible after login.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.x
- MySQL server

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the MySQL database:**

- Create a database named `flask`.
- Create a table named `users` with the following schema:

    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(120) NOT NULL,
        verified BOOLEAN DEFAULT 0,
        verification_token VARCHAR(255)
    );
    ```

5. **Update the application configuration:**

- Edit the `app.py` file to set your MySQL and email credentials:

    ```python
    app.config['MAIL_USERNAME']="your-email@gmail.com"
    app.config['MAIL_PASSWORD']="your-email-password"
    ```

- Replace `your-email@gmail.com` and `your-email-password` with your actual email and password.

## Running the Application

1. **Start the Flask development server:**

    ```bash
    python app.py
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

### Home Page

- The home page provides links to register, login, reset password, and forgot password functionalities.

### User Registration

- Navigate to the registration page to create a new account. You will need to verify your email address by clicking the verification link sent to your email.

### User Login

- After registering and verifying your email, you can log in using your username and password.

### Password Reset

- If you are logged in and wish to change your password, use the password reset functionality.

### Forgot Password

- If you have forgotten your password, use the forgot password functionality to reset it.


## Dependencies

- Flask
- Flask-WTF
- Flask-Bcrypt
- Flask-Mail
- MySQL Connector
- Itsdangerous

## Find the video here
https://www.youtube.com/watch?v=djQnt-SJ2Lc

