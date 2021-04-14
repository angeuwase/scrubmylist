"""
Defines the asynchronous tasks to be carried out in the background by celery
"""

from flask_mail import Message 
from . import mail, celery
from flask import current_app


@celery.task(name='app.tasks.send_celery_email', bind=True)
def send_celery_email(self,message_data):
    #app = current_app._get_current_object()

    #message = Message(subject=message_data['subject'],sender=app.config['MAIL_DEFAULT_SENDER'],  recipients= [message_data['recipients']], body= message_data['body'])
    message = Message(subject=message_data['subject'], recipients= [message_data['recipients']], html= message_data['html'])
    mail.send(message)

@celery.task(name='app.tasks.reverse_name', bind=True)
def reverse_name(self,name):
    return name[::-1]