from flask import jsonify, request, current_app, url_for
from . import api
from ..models import File


@api.route('/files/<int:id>')
def get_file(id):
    file = File.query.get_or_404(id)
    return jsonify(file.to_json())