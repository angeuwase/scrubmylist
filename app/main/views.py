from . import main_blueprint
from ..tasks import reverse_name
from flask import render_template

@main_blueprint.route('/')
def index():
    #result = reverse_name.apply_async(args=[name])
    return render_template('main/index.html')


@main_blueprint.route('/upload_email_list')
def upload_email_list():
    #result = reverse_name.apply_async(args=[name])
    return 'page under construction'