from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, HiddenField, TextAreaField
from wtforms.fields import EmailField, BooleanField

from .models import User


def codi_validator(form, field):

    if field.data.lower() == "codi":
        raise validators.ValidationError("This username is not allowed.")


def honeypot_length(form, field):
    if field.data:
        raise validators.ValidationError(
            'Only humans can fill this form!')


class LoginForm(Form):
    username = StringField("Username", [
        validators.length(min=4, max=50)
    ])
    password = PasswordField("Password", [
        validators.DataRequired(message="Password is a required field.")
    ])


class RegisterForm(Form):
    honeypot = HiddenField("", [
        honeypot_length
    ])
    username = StringField("Username", [
        validators.length(min=4, max=50),
        codi_validator
    ])
    email = EmailField("Email", [
        validators.length(min=6, max=100),
        validators.DataRequired(message="Email is a required field."),
        validators.Email(message="Please enter a valid email address.")
    ])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm_password",
                           message="Passwords do not match.")
    ])
    confirm_password = PasswordField("Confirm Password")
    accept = BooleanField("Accept Terms and Conditions", [
        validators.DataRequired()
    ])

    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError(
                "Username already in use.")

    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError(
                "Email address already in use.")


class TaskForm(Form):
    title = StringField("Title", [
        validators.length(min=4, max=50, message="Title length out of range"),
        validators.DataRequired(message="A task title is required.")
    ])
    description = TextAreaField("Description", [
        validators.DataRequired(message="A task description is required")
    ], render_kw={"rows": 6})
