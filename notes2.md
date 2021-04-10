# Environment variables required

FLASK_APP = app.py
FLASK_ENV = development
CONFIG_TYPE = config.DevelopmentConfig
SECRET_KEY = 
MAIL_USERNAME = 
MAIL_PASSWORD = 

# for local testing + single container
#CELERY_BROKER_URL = redis://localhost:6379
#RESULT_BACKEND = redis://localhost:6379

# for when all services are containerized 
CELERY_BROKER_URL = redis://redis:6379
RESULT_BACKEND = redis://redis:6379