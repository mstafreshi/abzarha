from flask import Blueprint

bp = Blueprint('notepad', __name__, template_folder='templates')

from . import routes