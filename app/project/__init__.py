from flask import Blueprint

project_bp = Blueprint("project_bp", __name__)

from . import routes