from flask import Blueprint

task_bp = Blueprint("task_bp", __name__)

from . import routes
