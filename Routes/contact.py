from flask import Blueprint, render_template, request, current_app
from datetime import datetime
from Controllers.db_handler import feedback
from config import load_config
from threading import Thread
from Controllers.email_handler import send_contact_email

# Define the Blueprint
contact_bp = Blueprint('contact', __name__)

# Load configuration
params = load_config()

def async_send_email(app, sender, recipient, subject, body):
    # Call the email handler with the app context
    send_contact_email(app, sender, recipient, subject, body)

@contact_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = "prateekaphale@gmail.com"
        phone = request.form['phone']
        message = request.form['message']
        date = datetime.now()

        # Save to database
        if feedback(Name=name, Email_address=email, Phone_number=phone, Message=message, Date=date):
            app = current_app._get_current_object()  # Get the actual Flask app instance
            thread = Thread(target=async_send_email, args=(
                app, email, params["Email_Information"]["mail_username"], "New Message From Blog", message
            ))
            thread.start()
            return render_template("contact.html", params=params, success=True)
        else:
            return render_template("contact.html", params=params, success=False)

    else:
        return render_template("contact.html", params=params, success=None)
