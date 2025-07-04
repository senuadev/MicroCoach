from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')

from . import routes  # noqa: E402, F401
