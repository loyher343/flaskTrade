from flask import Flask
from flask_mail import Mail, Message
from config import *
app = Flask(__name__)

app.config['DEBUG']= True
app.config['TESTING']=False
app.config['MAIL_SERVER']= MAIL_SERVER
app.config['MAIL_PORT']=PORT
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
#app.config['MAIL_DEBUG']=
app.config['MAIL_USERNAME']=EMAIL
app.config['MAIL_PASSWORD']=PASSWORD
app.config['MAIL_DEFAULT_SENDER']= EMAIL
app.config['MAIL_MAIL_MAX_EMAILS']=5
#app.config['MAIL_MAIL_SUPPRESS_SEND']=False
app.config['MAIL_ASCII_ATTACHMENTS']=False

mail = Mail(app)



@app.route('/mail')
def hello_world():
    msg = Message('YOOOO', recipients=[RECIPIENT])
    msg.html = '<b>This is the new test. yo</b>'
    mail.send(msg)
    return 'Message sent :)'

if __name__ == '__main__':
    app.run()
