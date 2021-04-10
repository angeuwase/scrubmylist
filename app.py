"""
This is where the flask application instance gets created and run
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()