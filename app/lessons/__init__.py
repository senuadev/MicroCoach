from flask import Blueprint

lessons_bp = Blueprint('lessons', __name__, template_folder='templates', url_prefix='/lessons')

from . import routes  # noqa: E402, F401
