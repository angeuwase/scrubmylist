from . import auth_blueprint

@auth_blueprint.route('/register')
def register():
    return 'Hello world from the auth blueprint'
