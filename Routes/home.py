from flask import Blueprint, render_template,request, session
from config import load_config
from Controllers.db_handler import get_posts
from Routes.user import logout
home_bp = Blueprint('home', __name__)

params = load_config()


@home_bp.route("/")
def home():

    page = request.args.get('page',1,type = int)
    per_page = 5
    post = get_posts(page=page,per_page=per_page)
    is_logged_in = session.get('is_logged_in', False)
    username = session.get('user',None)
    return render_template("index.html", params=params, posts=post,current_page = page,is_logged_in=is_logged_in, username = username)
