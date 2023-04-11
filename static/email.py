from static.extensions import mail
from flask import current_app,jsonify,render_template
from flask_mail import Message
from threading import Thread

from flask import url_for, current_app

def send_email_func(template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject="flask mail默认方式发送图片邮件", body="flask mail邮件测试",  recipients=["jlin@sicoresemi.com"])
    msg.html = render_template(template + '.html', **kwargs)
    with open("D:/001/line.png", "rb") as fp:
        msg.attach("image.png", "image/png", fp.read(), 'inline', headers=[('Content-ID', 'image')])
    send_async_email(app, msg)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_attach_mail(subject, to, html,attach):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    with current_app.open_resource(attach) as fp:
        message.attach("image.jpg", "image/jpg", fp.read(),'inline', headers=[('Content-ID', 'image')])
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr
