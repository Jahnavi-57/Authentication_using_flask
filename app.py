from flask import Flask, render_template,url_for,redirect,flash
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length,Email
from flask_bcrypt import Bcrypt
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a secret key"

#mysql connection
conn=mysql.connector.connect(host='localhost',user='root',password='oranje57',database='flask')
cursor=conn.cursor()

bcrypt=Bcrypt(app)

#Flask -Mail Configuration
app.config['MAIL_SERVER']="smtp.googlemail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']="oranjecloud@gmail.com"
app.config['MAIL_PASSWORD']="zxvo sbqo ihie ibbp"

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
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"username"})
    reset_password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"new password"})
    submit=SubmitField('Update password')
   
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
                return redirect(url_for('gallery'))
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
            return redirect(url_for('login'))
        else:
            error="Invalid username or old password"
            return render_template('reset_password.html',error=error,form=form)
        
    return render_template('reset_password.html',form=form)


@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        username=form.username.data
        rp=form.reset_password.data
        cursor.execute("select *from users where username=%s",(username,))
        user=cursor.fetchone()
        if user:
            hashed_new_password=bcrypt.generate_password_hash(rp).decode('utf-8')
            cursor.execute("update users set password=%s where username=%s",(hashed_new_password,username))
            conn.commit()
            return redirect(url_for('login'))
        else:
            error="Invalid username"
            return render_template('forgot_password.html',error=error,form=form)
        
    return render_template('forgot_password.html',form=form)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


#mail----
def send_verification_email(email,token):
    msg = Message('Email Verification', sender='your-email@gmail.com', recipients=[email])
    verification_url = url_for('verify_email', token=token, external=True)
    msg.html = f'''<p>To verify your email address, click the link below:</p>
    <p><a href="{request.host_url}{verification_url}">Verify Email Address</a></p>
    <p>If you did not create an account, please ignore this email.</p>'''  
    mail.send(msg)

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

if __name__ == "__main__":
    app.run(debug=True)
    cursor.close()
    conn.close()

