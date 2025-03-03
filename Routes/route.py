from flask import Blueprint, render_template
from Controllers.db_handler import get_db_connection
from config import load_config
post_bp = Blueprint('post', __name__)
params = load_config()

@post_bp.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM upload_blog WHERE id = %s"
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed to fetch the post."
    finally:
        cursor.close()

    if post is None:
        return "No post found."

    return render_template("post.html",params = params, post=post)
