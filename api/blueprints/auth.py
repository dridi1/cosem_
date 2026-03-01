from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from api.extensions import bcrypt, db
from api.forms import LoginForm, RegisterForm
from api.models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            remember = request.form.get("remember-me") == "on"
            login_user(user, remember=remember)
            return redirect(url_for("dashboard.private_dashboard"))
        error = "Invalid username or password. Please try again."
    return render_template("login.html", form=form, error=error)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login_fr", methods=["GET", "POST"])
def login_fr():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            remember = request.form.get("remember-me") == "on"
            login_user(user, remember=remember)
            return redirect(url_for("dashboard.private_dashboard_fr"))
        error = "Identifiants invalides. Veuillez reessayer."
    return render_template("login_fr.html", form=form, error=error)


@auth_bp.route("/logout_fr")
@login_required
def logout_fr():
    logout_user()
    return redirect(url_for("auth.login_fr"))


@auth_bp.route("/register_fr", methods=["GET", "POST"])
def register_fr():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription reussie. Veuillez vous connecter.", "success")
        return redirect(url_for("auth.login_fr"))
    return render_template("register_fr.html", form=form)
