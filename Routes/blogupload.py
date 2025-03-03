from flask import Blueprint, render_template, request,current_app
from datetime import datetime
from Controllers.db_handler import save_blog_post
from config import load_config
from threading import Thread
from Controllers.email_handler import send_contact_email
blogupload_bp = Blueprint('blogupload', __name__)

params = load_config()
def async_send_email(app,sender, recipient, subject, body):
    send_contact_email(app,sender=sender, recipient=recipient, subject=subject, body=body)

@blogupload_bp.route("/blogupload", methods=['GET', 'POST'])
def blogupload():
    if request.method == 'POST':
        title = request.form['title']
        email = request.form['email']
        content = request.form['content']
        author = request.form['name']
        date = datetime.now()
        # Save blog post to the database
        if save_blog_post(title, content, date, author, email):
            app = current_app._get_current_object()
            thread = Thread(target=async_send_email, args=(
                app,params["Email_Information"]["mail_username"],email,"Blog Uploaded Successfully ! ","Your blog has been posted successfully on Supernatural Blogs! "
            "Keep visiting our blog site to check the impact of your blog. 😀"
            ))
            thread.start()
            return render_template("blogupload.html",params=params,success = True)
        else:
            return render_template("blogupload.html", params=params, success=False)

    return render_template("blogupload.html", params=params)
