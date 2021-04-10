from . import main_blueprint
from ..tasks import reverse_name

@main_blueprint.route('/<name>')
def index(name):
    result = reverse_name.apply_async(args=[name])
    return 'Hello world from main blueprint'