from . import dashboard_bp
from flask import render_template, request, jsonify
from models import Project, Task

@dashboard_bp.get('/analytics')
def analytics():
    projectCount = Project.count()
    taskCount = Task.count()

    data = {
        "projectCount": projectCount,
        "taskCount": taskCount            
    }

    return jsonify({"status": "success", "message": "Dashboard Analytics Data Retrieved Successfully.", "data": data})