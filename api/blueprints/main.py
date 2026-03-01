from flask import Blueprint, flash, redirect, render_template, url_for

from api.extensions import db
from api.forms import ContactForm
from api.models import ContactMessage


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home_fr():
    return render_template("home_fr.html")


@main_bp.route("/en")
def home():
    return render_template("home.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/about_fr")
def about_fr():
    return render_template("about_fr.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        save_contact_message(form)
        flash("Thank you for submitting your message!")
        return redirect(url_for("main.thnx_for_submit"))
    return render_template("contact.html", form=form)


@main_bp.route("/contact_fr", methods=["GET", "POST"])
def contact_fr():
    form = ContactForm()
    if form.validate_on_submit():
        save_contact_message(form)
        flash("Merci pour votre message!")
        return redirect(url_for("main.thnx_for_submit_fr"))
    return render_template("contact_fr.html", form=form)


@main_bp.route("/thnx")
def thnx_for_submit():
    return render_template("thnx_for_submit.html")


@main_bp.route("/merci")
def thnx_for_submit_fr():
    return render_template("thnx_for_submit_fr.html")


@main_bp.route("/gallery")
def gallery():
    return render_template("gallery.html")


@main_bp.route("/Galerie")
def gallery_fr():
    return render_template("gallery_fr.html")


@main_bp.route("/Cereals_Catalog")
def cereals_catalog():
    return render_template("Cereals_Catalog.html")


@main_bp.route("/Cereals_Catalog_fr")
def cereals_catalog_fr():
    return render_template("Cereals_Catalog_fr.html")


def save_contact_message(form):
    new_message = ContactMessage(
        name=form.name.data,
        email=form.email.data,
        subject=form.subject.data,
        message=form.message.data,
    )
    db.session.add(new_message)
    db.session.commit()
