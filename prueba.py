from flask import Flask
from flask.ext.mail import Mail, Message

app =Flask(__name__)
mail=Mail(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'diaz2209@gmail.com',
    MAIL_PASSWORD = '22091994',
))

mail=Mail(app)

@app.route("/")
def index():
  msg = Message(
              'Hello',
         sender='diaz2209@gmail.com',
         recipients=
               ['diaz2209@gmail.com'])
  msg.body = "Este es el mensaje"
  mail.send(msg)
  return "Sent"

if __name__ == "__main__":
    app.run( host = '0.0.0.0', port = 5001 )