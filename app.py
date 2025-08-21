from flask import Flask, render_template,url_for,redirect
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length,Email
from flask_bcrypt import Bcrypt
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer
from flask import request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a secret key"

#mysql connection
conn= mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME'),
    port=int(os.environ.get('DB_PORT',3306)),
    ssl_ca=os.path.join(os.path.dirname(__file__), "ca.pem")
)
cursor = conn.cursor()

bcrypt=Bcrypt(app)

#Flask -Mail Configuration
app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']="oranjecloud@gmail.com"
app.config['MAIL_PASSWORD']="kzme hjow uqql eltr"

mail=Mail(app)

class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"password"})
    email = StringField(validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)], render_kw={'placeholder': "email"})
    submit=SubmitField("Register")
    

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"password"})
    submit=SubmitField("Login")

class ResetPasswordForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"username"})
    old_password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"old password"})
    new_password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"new password"})
    submit=SubmitField('Reset')

class ForgotPasswordForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)], render_kw={'placeholder': "email"})
    submit=SubmitField('Send Password Reset link')

class ChangePasswordForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"username"})
    new_password= PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"new password"})
    submit=SubmitField('Update Password')

   
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        cursor.execute("select *from users where username=%s",(username,))
        user = cursor.fetchone()
        if user:
            if bcrypt.check_password_hash(user[2], password):
                if user[4]==1: #only verified users
                    return redirect(url_for('gallery'))
                else:
                    return render_template("login.html",form=form,error="Please verify your email before logging in")
            else:
                return render_template("login.html",form=form,error="Wrong password")
        else:
            return render_template("login.html",form=form,error="user does not exist")
        
    return render_template('login.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username=form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email=form.email.data
        verification_token=generate_verification_token(email)
        cursor.execute("select *from users where username=%s",(username,))
        user=cursor.fetchone()
        if user:
            return render_template('register.html',form=form,error="username exists,choose different one")
        else:
            cursor.execute("insert into users(username, password,email,verified,verification_token)values(%s,%s,%s,%s,%s)",(username, hashed_password,email,0,verification_token))
            conn.commit()
            send_verification_email(email,verification_token)
            return render_template('register.html',form=form,success="please check ur mail to verify email")

    return render_template('register.html', form=form)


@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
    form=ResetPasswordForm()
    if form.validate_on_submit():
        username=form.username.data
        op=form.old_password.data
        np=form.new_password.data
        cursor.execute("select *from users where username=%s",(username,))
        user=cursor.fetchone()
        if user and bcrypt.check_password_hash(user[2],op):
            hashed_new_password=bcrypt.generate_password_hash(np).decode('utf-8')
            cursor.execute("update users set password=%s where username=%s",(hashed_new_password,username))
            conn.commit()
            msg="Password Reset Successful"
            return render_template('reset_password.html',msg=msg,form=form)
        else:
            error="Invalid username or old password"
            return render_template('reset_password.html',error=error,form=form)
        
    return render_template('reset_password.html',form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email= form.email.data
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user:
            token = serializer.dumps(email, salt='password-reset')
            reset_link = url_for('change_password', token=token, _external=True)

            msg = Message('Password Reset Request',
                          sender='oranjecloud@gmail.com',
                          recipients=[email])
            msg.html = f'''
            <p>To rest your password, click the link below:</p>
            <p><a href="{reset_link}">Reset Password</a></p>
            <p>If you did not create an account, please ignore this email.</p>'''
            mail.send(msg)

            success="Reset Link sent to your email"
            return render_template('forgot_password.html', success=success,form=form)
        else:
            error = "Invalid username"
            return render_template('forgot_password.html', error=error,form=form)
    
    return render_template('forgot_password.html',form=form)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username=form.username.data
        np= form.new_password.data
        cursor.execute("select *from users where username=%s",(username,)) 
        user=cursor.fetchone() 
        if user:
            hashed_new_password=bcrypt.generate_password_hash(np).decode('utf-8')
            cursor.execute("update users set password=%s where username=%s",(hashed_new_password,username))
            conn.commit()
            msg="Password Update Successful"
            return render_template('change_password.html',msg=msg,form=form)
        else:
            error="Invalid username"
            return render_template('change_password.html',error=error,form=form)
        
    return render_template('change_password.html',form=form)
            

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


#Email Verification---
#-----------------------------------------------------------------------------------------
def send_verification_email(email, token):
    verification_url = url_for('verify_email', token=token, _external=True)
    msg = Message(
        'Email Verification',
        sender='oranjecloud@gmail.com',   # must match MAIL_USERNAME
        recipients=[email]
    )
    msg.html = f'''
        <p>To verify your email address, click the link below:</p>
        <p><a href="{verification_url}">Verify Email Address</a></p>
        <p>If you did not create an account, please ignore this email.</p>
    '''
    try:
        mail.send(msg)
        print(f"✅ Verification email sent to {email}")
    except Exception as e:
        print("❌ Email failed:", str(e))


serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_verification_token(email):
    return serializer.dumps({'email': email})

# Verify the token
def verify_verification_token(token):
    try:
        data = serializer.loads(token)
        email = data.get('email')
    except:
        return None
    return email


@app.route("/verify_email/<token>")
def verify_email(token):
    email=verify_verification_token(token)
    if email:
        cursor.execute("update users set verified=1 where email=%s",(email,))
        conn.commit
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))
#Reset token generation and verification---------------------------------------------------------

def generate_reset_token(email, secret_key, expires_sec=1800):  # 30 min expiry
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps(email, salt='password-reset')

def verify_reset_token(token, secret_key, expires_sec=1800):
    s = URLSafeTimedSerializer(secret_key)
    try:
        email = s.loads(token, salt='password-reset', max_age=expires_sec)
    except:
        return None
    return email

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
    cursor.close()
    conn.close()

