from flask import jsonify, session, request
from . import project_bp
from models import Project
from datetime import datetime

@project_bp.post('/add')
def addProject():

    current_user = session["project"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')


    if name == "" or description =="":
         return jsonify({"status":"error","message":"Name and Description is required!"})
    
    project = Project(
        name = name,
        description = description
    )

    project.save()

    return jsonify({"status": "success", "message": "Project Added successfully."})


@project_bp.put('/update')
def updateProject():

    current_user = session["project"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    project = Project.objects(id=id).first()
    
    if not project:
        return jsonify({"status": "error", "message": "User not found."})

    
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    
    
    Project.name = name
    Project.description = description
    Project.updatedTime = datetime.now()

    Project.save()

    return jsonify({"status": "success", "message": "Project  Updated successfully."})

@project_bp.delete('/delete')
def deleteProject():

    current_user = session["project"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    project = Project.objects(id=id).first()
    
    if not project:
        return jsonify({"status": "error", "message": "User not found."})

    Project.delete()

    return jsonify({"status": "success", "message": "project deleted successfully."})


@project_bp.get('/getSingle')
def getSingleProject():
    
    current_user = session["project"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    project = Project.objects(id=id).first()
    
    if not project:
        return jsonify({"status": "error", "message": "User not found."})
    
    actual_data = {
        "name":  Project.name,
        "description":  Project.description,
        "addedTime":  Project.addedTime,
        "updatedTime":  Project.updatedTime
    }

    return jsonify({"status": "success", "message": "Project Retrieved Successfully", "data": actual_data})

@project_bp.get('/getMany')
def getMany():
    
    current_user = session["project"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    projects = Project.objects()

    actual_data = []

    for project in projects:
        data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "addedTime": project.addedTime,
            "updatedTime": project.updatedTime
            
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "Project Retrieved Successfully", "data": actual_data})