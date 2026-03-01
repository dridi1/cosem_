from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError

from api.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(message="Username is required"), Length(min=3, max=20)],
        render_kw={"placeholder": "Username"},
    )
    email = StringField(
        "Email",
        validators=[InputRequired(message="Email is required"), Email(message="Enter a valid email address")],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired(message="Password is required"), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[InputRequired(), EqualTo("password", message="Passwords must match")],
        render_kw={"placeholder": "Confirm Password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("That email already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    subject = TextAreaField("Subject", validators=[InputRequired(), Length(min=1)])
    message = TextAreaField("Message", validators=[InputRequired(), Length(min=1)])
    submit = SubmitField("Submit")
