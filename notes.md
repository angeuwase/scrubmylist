# Problems with celery when trying to send email

## Code
app/tasks.py
```
from flask_mail import Message 
from . import mail, celery
from flask import current_app


@celery.task(name='app.tasks.send_celery_email', bind=True)
def send_celery_email(self,message_data):
    app = current_app._get_current_object()

    message = Message(subject=message_data['subject'],sender=app.config['MAIL_DEFAULT_SENDER'],  recipients= [message_data['recipients']], body= message_data['body'])
    message = Message(subject=message_data['subject'], recipients= [message_data['recipients']], body= message_data['body'])
    mail.send(message)
```

app/auth/views.py
```
from . import auth_blueprint
from ..tasks import send_celery_email

@auth_blueprint.route('/register/<email>')
def register(email):
    message_data = {
        'subject': 'Hello from Flask',
        'body': 'This email was send asynchronously using celery',
        'recipients': email
    }

    send_celery_email.apply_async(args=[message_data])

    return 'Hello world from the auth blueprint'
```

command ran to start celery worker:
```
 celery -A celery_worker.celery worker --pool=gevent --concurrency=500 --loglevel=debug
```

## error message when i called this task:
```
[2021-04-10 12:25:58,813: INFO/MainProcess] Received task: app.tasks.send_celery_email[8ea8be5e-2ea2-40ae-8274-795c147f67e7]  
[2021-04-10 12:25:58,814: DEBUG/MainProcess] TaskPool: Apply <function _trace_task_ret at 0x0472F6E8> (args:('app.tasks.send_celery_email', '8ea8be5e-2ea2-40ae-8274-795c147f67e7', {'lang': 'py', 'task': 'app.tasks.send_celery_email', 'id': '8ea8be5e-2ea2-40ae-8274-795c147f67e7', 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'retries': 0, 'timelimit': [None, None], 'root_id': '8ea8be5e-2ea2-40ae-8274-795c147f67e7', 'parent_id': None, 'argsrepr': "[{'subject': 'Hello from Flask', 'body': 'This email was send asynchronously using celery', 'recipients': '11anguwa@gmail.com'}]", 'kwargsrepr': '{}', 'origin': 'gen21416@LAPTOP-MKMU5ESC', 'reply_to': '143687e2-0a4e-3c0e-9d77-f359545360d0', 'correlation_id': '8ea8be5e-2ea2-40ae-8274-795c147f67e7', 'hostname': 'celery@LAPTOP-MKMU5ESC', 'delivery_info': {'exchange': '', 'routing_key': 'celery', 'priority': 0, 'redelivered': None}, 'args': [{'subject': 'Hello from Flask', 'body': 'This email was send asynchronously using celery', 'recipients': '11anguwa@gmail.com'}], 'kwargs': {}}, b'[[{"subject": "Hello from Flask", "body": "This email was... kwargs:{})
[2021-04-10 12:25:58,816: DEBUG/MainProcess] Task accepted: app.tasks.send_celery_email[8ea8be5e-2ea2-40ae-8274-795c147f67e7] pid:13708
[2021-04-10 12:25:58,828: ERROR/MainProcess] Task app.tasks.send_celery_email[8ea8be5e-2ea2-40ae-8274-795c147f67e7] raised unexpected: RuntimeError('Working outside of application context.\n\nThis typically means that you attempted to use functionality that needed\nto interface with the current application object in some way. To solve\nthis, set up an application context with app.app_context().  See the\ndocumentation for more information.')
Traceback (most recent call last):
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\celery\app\trace.py", line 405, in trace_task
    R = retval = fun(*args, **kwargs)
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\celery\app\trace.py", line 697, in __protected_call__
    return self.run(*args, **kwargs)
  File "C:\projects-directory\scrubmylist\app\tasks.py", line 12, in send_celery_email
    app = current_app._get_current_object()
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\werkzeug\local.py", line 306, in _get_current_object
    return self.__local()
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\flask\globals.py", line 52, in _find_app
    raise RuntimeError(_app_ctx_err_msg)
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
to interface with the current application object in some way. To solve
this, set up an application context with app.app_context().  See the
documentation for more information.

```

## Tried removing reference to sender as i had already configured a default sender in config.py
Code:
```
@celery.task(name='app.tasks.send_celery_email', bind=True)
def send_celery_email(self,message_data):
    #app = current_app._get_current_object()

    #message = Message(subject=message_data['subject'],sender=app.config['MAIL_DEFAULT_SENDER'],  recipients= [message_data['recipients']], body= message_data['body'])
    message = Message(subject=message_data['subject'], recipients= [message_data['recipients']], body= message_data['body'])
    mail.send(message)
```

Same error:
```
[2021-04-10 12:28:56,158: INFO/MainProcess] Received task: app.tasks.send_celery_email[b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67]  
[2021-04-10 12:28:56,158: DEBUG/MainProcess] TaskPool: Apply <function _trace_task_ret at 0x03E6F6E8> (args:('app.tasks.send_celery_email', 'b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67', {'lang': 'py', 'task': 'app.tasks.send_celery_email', 'id': 'b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67', 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'retries': 0, 'timelimit': [None, None], 'root_id': 'b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67', 'parent_id': None, 'argsrepr': "[{'subject': 'Hello from Flask', 'body': 'This email was send asynchronously using celery', 'recipients': '11anguwa@gmail.com'}]", 'kwargsrepr': '{}', 'origin': 'gen8312@LAPTOP-MKMU5ESC', 'reply_to': 'f8416f65-9db2-38c0-aedb-223a69e6f8cb', 'correlation_id': 'b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67', 'hostname': 'celery@LAPTOP-MKMU5ESC', 'delivery_info': {'exchange': '', 'routing_key': 'celery', 'priority': 0, 'redelivered': None}, 'args': [{'subject': 'Hello from Flask', 'body': 'This email was send asynchronously using celery', 'recipients': '11anguwa@gmail.com'}], 'kwargs': {}}, b'[[{"subject": "Hello from Flask", "body": "This email was... kwargs:{})
[2021-04-10 12:28:56,171: DEBUG/MainProcess] Task accepted: app.tasks.send_celery_email[b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67] pid:11760
[2021-04-10 12:28:56,184: ERROR/MainProcess] Task app.tasks.send_celery_email[b0e3b5d4-f80d-40dd-b7e6-22c3f2a15e67] raised unexpected: RuntimeError('Working outside of application context.\n\nThis typically means that you attempted to use functionality that needed\nto interface with the current application object in some way. To solve\nthis, set up an application context with app.app_context().  See the\ndocumentation for more information.')
Traceback (most recent call last):
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\celery\app\trace.py", line 405, in trace_task
    R = retval = fun(*args, **kwargs)
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\celery\app\trace.py", line 697, in __protected_call__
    return self.run(*args, **kwargs)
  File "C:\projects-directory\scrubmylist\app\tasks.py", line 15, in send_celery_email
    message = Message(subject=message_data['subject'], recipients= [message_data['recipients']], body= message_data['body'])
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\flask_mail.py", line 273, in __init__
    sender = sender or current_app.extensions['mail'].default_sender
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\werkzeug\local.py", line 347, in __getattr__
    return getattr(self._get_current_object(), name)
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\werkzeug\local.py", line 306, in _get_current_object
    return self.__local()
  File "c:\projects-directory\scrubmylist\env\lib\site-packages\flask\globals.py", line 52, in _find_app
    raise RuntimeError(_app_ctx_err_msg)
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
to interface with the current application object in some way. To solve
this, set up an application context with app.app_context().  See the
documentation for more information.
```

## Changed the execution pool from gevent to solo
command:
```
 celery -A celery_worker.celery worker --pool=solo --loglevel=info
```
And it worked!