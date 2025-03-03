from flask import Blueprint, render_template
from config import load_config

# Define the Blueprint
about_bp = Blueprint('about', __name__)

# Load configuration
params = load_config()

@about_bp.route("/about")
def about():
    return render_template("about.html", params=params)
