from flask import Flask
from Controllers import  email_handler
from Routes.home import home_bp  # Import home blueprint
from Routes.about import about_bp
from Routes.contact import contact_bp
from Routes.blogupload import blogupload_bp
from Routes.route import post_bp
from Routes.user import user_bp
from config import config_app,load_config

app = Flask(__name__)


config_app(app)
params = load_config()
app.secret_key = params["Session"]["secret_key"]

email_handler.mail.init_app(app)

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(about_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(blogupload_bp)
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
