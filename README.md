# Flask Authentication App
This is a Flask-based web application that provides user registration, login, email verification, password reset, and forgot password functionalities. It uses MySQL as the database, Flask-Mail for email verification, and Flask-WTF for form handling.

## 🌟 Motivation & Journey  

I had been trying to deploy my Flask applications for a long time , but always found the process tricky and incomplete. Today, I discovered **Render** and decided to give it another try. From morning till now, I kept experimenting, debugging, and retrying. 

### Deployment Completed At: 
![Deployment Time](https://img.shields.io/badge/Deployed%20On-21%20Aug%202025%20|%2011:04%20PM%20IST-success?style=for-the-badge)


Finally, I successfully deployed my Flask application with a **managed MySQL database on Aiven**. This journey was not just about finishing the project—it was about persistence. I kept trying until I got it right, and now I’m really happy that I learned how to deploy a full **Flask + MySQL app** with email features and database hosting! 🎉  

## Features

- User Registration & Login
- Password Hashing using bcrypt for security 
- Email Verification
- Password Reset with Token
- Secure Forgot Password and Reset Password Functionalities
- Deployment on **Render** with a **managed MySQL database (Aiven)** 

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
4. **🗄️Database Setup (Aiven MySQL)**
    1. Sign up at Aiven
    2. Create a MySQL Database → choose Free-1-1gb plan.
    3. Download the CA Certificate (ca.pem) and add to the project folder.
    4. Connect using MySQL client:
       
    ```bash
       mysql -h <your-Aiven-host> -P <port> -u <username> -p --ssl-ca="path/to/ca.pem" defaultdb
    ```
    5. Create your table:
   
    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        verified BOOLEAN DEFAULT FALSE,
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
  
6. **🌍 Deployment on Render**
   
    1. Push your code to GitHub.
    2. Go to Render Dashboard
    3. Click New Web Service → Connect your GitHub repo.
    4. In Build & Deploy Settings:
        -  Build Command:
          
            ```bash
            pip install -r requirements.txt
            ```
        - Start Command:
          
            ```bash
            gunicorn app:app
            ```
    5. Add Environment Variables in Render → Settings → Environment:
   
        ```ini
        FLASK_APP=app.py
        FLASK_ENV=production
        SECRET_KEY=<your_secret_key>
        
        DB_HOST=<your Aiven host>
        DB_PORT=<your Aiven port>
        DB_USER=<your Aiven username>
        DB_PASSWORD=<your Aiven password>
        DB_NAME=defaultdb
        
        MAIL_SERVER=smtp.gmail.com
        MAIL_PORT=587
        MAIL_USERNAME=<your email>
        MAIL_PASSWORD=<your email password>
        
        ```
    7. Deploy 🎉

   
## 🌍 Live Demo
- Deployed on Render : [Click this for live demo](https://authentication-using-flask-zjfj.onrender.com/)

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

## 🌟 Key Highlights

- 🔒 Secure Authentication Flow – Passwords are hashed using bcrypt for safe storage.

- 📧 Verified Accounts – Email-based verification ensures only trusted users gain access.

- 🔑 Token-Based Password Reset – Protects against unauthorized resets using time-bound tokens.

- 🛡️ Encrypted Database Connection – MySQL hosted on Aiven, connected over SSL (ca.pem) for data security.

☁️ Cloud Deployment – Deployed on Render, ensuring availability without local server dependency.
## Dependencies

- Flask
- Flask-WTF
- Flask-Bcrypt
- Flask-Mail
- MySQL Connector
- Itsdangerous
  
## 🛠️ Tech Stack

- Backend: Flask (Python)
- Database: MySQL (Aiven)
- Deployment: Render
- Security: SSL + Tokens

## 🔮 Future Improvements

- Role-based Access Control (Admin/User)
- JWT Authentication
- CI/CD pipeline for automated deployment
- Improved UI

## Find the video here

[Previous Version Video available here](https://www.youtube.com/watch?v=djQnt-SJ2Lc)

