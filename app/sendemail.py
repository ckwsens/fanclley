#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from app import celery,create_app
from . import mail
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#@celery.task
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

    #return {'status': 'Send task done!'}


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FANCLLEY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FANCLLEY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

#@celery.task
def sendto_kindle(to, bookname):
    #搞一个局部的app。
    app = create_app('production')
    msg = Message(app.config['FANCLLEY_MAIL_SUBJECT_PREFIX']+ ' ' + u'Your book coming!',
                  sender=app.config['FANCLLEY_MAIL_SENDER'], recipients=[to])
    msg.body = u"fanclley"
    msg.html = u"<b>Fanclley provide this service for you!</b>"
    with app.open_resource(u"data/mobiworkshop/" + bookname + u'.mobi') as fp:
        msg.attach(u'fanclley.mobi', "*/*", fp.read())
    #mail.send()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
