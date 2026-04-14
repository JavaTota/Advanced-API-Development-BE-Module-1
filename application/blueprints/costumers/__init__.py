from flask import Blueprint

costumer_bp = Blueprint('costumer', __name__)

from . import routes