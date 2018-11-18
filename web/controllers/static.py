from flask import Blueprint, send_from_directory
from application import app

route_static = Blueprint('static', __name__)


@route_static.route('/<path:filename>')
def filename(filename):
    #app.logger.info("fuxb --> filename:" + filename)
    return send_from_directory(app.root_path + '/web/static/', filename)
