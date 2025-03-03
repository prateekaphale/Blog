import json


def load_config():
    with open('C:\FLASK BLOG\config.json','r') as file:
        config = json.load(file)["prams"]
    return config
def config_app(app):
    params = load_config()
    app.config.update(params)
    app.config['MAIL_SERVER'] = params['Email_Information']['mail_server']
    app.config['MAIL_PORT'] = params['Email_Information']['mail_port']
    app.config['MAIL_USERNAME'] = params["Email_Information"]["mail_username"]
    app.config['MAIL_PASSWORD'] = "lkqi rhfq jybi bcia"
    app.config['MAIL_USE_SSL'] = True