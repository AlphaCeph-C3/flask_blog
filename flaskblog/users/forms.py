from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, EmailField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                ValidationError)

from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=2, max=20)],
    )
    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(min=3, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[InputRequired(), EqualTo("password")],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is taken. Please choose a different one."
            )


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(min=3, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8)],
    )
    remember = BooleanField("Remember Me!")
    submit = SubmitField("Login")


class AccountUpdateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=2, max=20)],
    )
    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(min=3, max=25)],
    )
    picture = FileField(
        "Update Profile Picture",
        validators=[
            FileAllowed(
                upload_set=["jpg", "png"],
                message="Images Only! Please upload a image file with valid extension of either .jpg  or .png",
            )
        ],
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "This username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "This email is taken. Please choose a different one."
                )


class RequestResetForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Request Passsword Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[InputRequired(), EqualTo("password")],
    )
    submit = SubmitField("Reset Password")
