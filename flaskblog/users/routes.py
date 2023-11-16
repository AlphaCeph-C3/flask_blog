from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import bcrypt, db
from flaskblog.models import Post, User
from flaskblog.users.forms import (AccountUpdateForm, LoginForm,
                                   RegistrationForm, RequestResetForm,
                                   ResetPasswordForm)
from flaskblog.users.utils import delete_old_pp, save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "Your account has been created! You are now able to log in",
            category="success",
        )
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.home"))
            )
        else:
            flash(
                "Login Unsuccessful. Please check email and password",
                category="danger",
            )
    return render_template("login.html", form=form, title="Login")


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountUpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # deleting the old profile pics so that cluster of profile pics don't gather around
            if current_user.image_file != "default.jpg":
                try:
                    delete_old_pp(current_user.image_file)
                except FileNotFoundError:
                    pass
            # saving the profile picture you just updated
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", category="success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename=f"profile_pics/{current_user.image_file}"
    )
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_post(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(per_page=5, page=page)
    )
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
        except AttributeError:
            pass
        finally:
            flash(
                f"If an account with the email address '{form.email.data}'"
                " exists. A password reset email will be sent to it shortly.",
                "info",
            )
            return redirect(url_for("users.login"))
    return render_template(
        "request_reset.html", title="Reset Password", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash(
            "That is a invalid or expired Token, Please start the process again",
            "warning",
        )
        return redirect(url_for("users.request_reset"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(
            "Your password has been updated! You are now able to login",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "reset_token.html", title="Reset Password", form=form
    )
