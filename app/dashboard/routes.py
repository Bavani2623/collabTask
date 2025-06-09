from . import dashboard_bp
from flask import jsonify, session
from models import Project, Task

@dashboard_bp.get('/analytics')
def analytics():
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    projectCount = Project.objects().count()
    taskCount = Task.objects().count()

    data = {
        "projectCount": projectCount,
        "taskCount": taskCount            
    }

    return jsonify({"status": "success", "message": "Dashboard Analytics Data Retrieved Successfully.", "data": data})