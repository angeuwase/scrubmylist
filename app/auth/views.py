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
