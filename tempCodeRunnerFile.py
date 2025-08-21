class ForgotPasswordForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)], render_kw={'placeholder': "email"})
    submit=SubmitField('Send Password Reset link')