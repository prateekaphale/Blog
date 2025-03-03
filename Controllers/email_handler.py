from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_contact_email(app, sender, recipient, subject, body):
    # Use the provided app's context to send the email
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=[recipient])
        msg.body = body
        mail.send(msg)
