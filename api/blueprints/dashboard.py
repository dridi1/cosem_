import json

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from api.extensions import db
from api.models import Polygon
from api.services import build_analysis_context, normalize_coordinates


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/private_dashboard")
@login_required
def private_dashboard():
    return render_template("private_dashboard.html")


@dashboard_bp.route("/private_dashboard_fr")
@login_required
def private_dashboard_fr():
    return render_template("private_dashboard_fr.html")


@dashboard_bp.route("/analyze")
@login_required
def analyze():
    return render_template("analyze.html")


@dashboard_bp.route("/analyse_fr")
@login_required
def analyse_fr():
    return render_template("analyse_fr.html")


@dashboard_bp.route("/yourdash")
@login_required
def yourdash():
    return render_template("yourdash.html", **build_analysis_context(request))


@dashboard_bp.route("/yourdash_fr")
@login_required
def yourdash_fr():
    return render_template("yourdash_fr.html", **build_analysis_context(request))


@dashboard_bp.route("/public_dashboard")
def public_dashboard():
    return render_template("public_dashboard.html")


@dashboard_bp.route("/public_dashboard_fr")
def public_dashboard_fr():
    return render_template("public_dashboard_fr.html")


@dashboard_bp.route("/save_polygon", methods=["POST"])
@login_required
def save_polygon():
    data = request.get_json(silent=True) or {}
    coordinates = normalize_coordinates(data.get("coordinates"))

    if coordinates is None:
        return jsonify({"status": "error", "message": "Invalid coordinates payload"}), 400

    polygon = Polygon(coordinates=json.dumps(coordinates))
    db.session.add(polygon)
    db.session.commit()

    return jsonify({"status": "success", "coordinates": coordinates})
