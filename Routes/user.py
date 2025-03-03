from flask import Blueprint, render_template, request, session, redirect, url_for
from config import load_config

# Define the Blueprint
user_bp = Blueprint('user', __name__)

# Load configuration
params = load_config()

@user_bp.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['pass']
        if username == params['user'] and password == params['pass']:
            session['is_logged_in'] = True
            session['user'] = username[:7]
            return redirect(url_for('home.home'))
        else:
            return render_template("signin1.html", params=params, success=False)
    else:
        return render_template("signin1.html", params=params, success= None)

@user_bp.route("/logout")
def logout():
    session.pop('is_logged_in',None)
    session.pop('username',None)
    return redirect(url_for('home.home'))

@user_bp.route("/profile")
def profile():
    if not session.get('is_logged_in'):
        return redirect(url_for('user.user'))
    return render_template("profile.html", username=session.get('username'))
