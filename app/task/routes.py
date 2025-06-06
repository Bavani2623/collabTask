from flask import jsonify, session, request
from . import task_bp
from models import Task, User
from datetime import datetime

@task_bp .post('/add')
def addtask():

    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    status = data.get('status')

    if name == "" or description =="" or description =="" or status =="":
         return jsonify({"status":"error","message":"all data is required!"})
    
    task = Task(
        name = name,
        description = description,
        status = status        
    )

    task.save()

    return jsonify({"status": "success", "message": "Task Added successfully."})


@task_bp.put('/update')
def updateTask():

    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    task = Task.objects(id=id).first()
    if not task:
        return jsonify({"status": "error", "message": "Task not found."})
    
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    status = data.get('status')

    if name == "" or description =="" or status =="":
        return jsonify({"status":"error","message":"all data is required!"})
    
    task.name = name
    task.description = description
    task.status = status
    task.updatedTime = datetime.now()

    task.save()

    return jsonify({"status": "success", "message": "Task  Updated successfully."})

@task_bp.delete('/delete')
def deleteTask():

    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    task = Task.objects(id=id).first()
    if not task:
        return jsonify({"status": "error", "message": "Task not found."})
    
    Task.delete()

    return jsonify({"status": "success", "message": "Task deleted successfully."})


@task_bp.get('/getSingle')
def getSingletask():
    
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    task = task.objects(id=id).first()
    if not task:
        return jsonify({"status": "error", "message": "Task not found."})
    
    actual_data = {
    
        "name": task.name,
        "description": task.description,
        "status": task.status,
        "addedTime": task.addedTime,
        "updatedTime": task.updatedTime
    }

    return jsonify({"status": "success", "message": "Task Retrieved Successfully", "data": actual_data})

@task_bp.get('/getMany')
def getMany():
    
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    tasks= Task.objects()

    actual_data = []

    for task in tasks:
        data = {
            
            "name":task.name,       
            "description":task.description,
            "status":task.status,
            "addedTime":task.addedTime,
            "updatedTime":task.updatedTime
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "Task Retrieved Successfully", "data": actual_data})


@task_bp.put('/updateStatus')
def updateTaskStatus():
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    task = Task.objects(id=id).first()
    if not task:
        return jsonify({"status": "error", "message": "Task not found."})
    
    data = request.get_json()
    status = data.get('status')

    if  status == "" :
        return jsonify({"status":"error","message":"status is required!"})
    
    task.status = status

    task.save()

    return jsonify({"status": "success", "message": "Task  Updated successfully."})


@task_bp.put('/assignTask')
def assignTask():
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    data = request.get_json()
    
    assignedTo = data.get('assignedTo')
    taskList = data.get('taskList')

    user = User.objects(id=assignedTo).first()
    if not user:
        return jsonify({"status":"error","Message":"User not found"})

    for task in taskList:
        task = Task.objects(id=task).first()
        if not task:
            return jsonify({"status":"error","Message":"Task not found"})          
        
        task.assignedTo = user

    return jsonify({"status":"success","Message":"Task Assigned Successfully"})

@task_bp.get('/getAllNames')
def getAllNames():
    
    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    tasks= Task.objects()

    actual_data = []

    for task in tasks:
        data = {

            "id": task.id,
            "name":task.name        
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "Task Retrieved Successfully", "data": actual_data})
