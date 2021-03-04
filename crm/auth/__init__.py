from flask import Blueprint

bp = Blueprint('auth', __name__)


from crm.auth import routes