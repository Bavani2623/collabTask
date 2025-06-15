from flask import jsonify, session, request
from . import task_bp
from models import Task, User
from datetime import datetime, timedelta
from mongoengine import Q

@task_bp .post('/add')
def addtask():

    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    status = str(data.get('status'))

    if name == "" or description =="" or description =="":
         return jsonify({"status":"error","message":"all data is required!"})
    
    task = Task(
        name = name,
        description = description,
        status = "assigned" if status == '' else status.lower()       
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
    status = str(data.get('status'))

    if name == "" or description =="":
        return jsonify({"status":"error","message":"all data is required!"})
    
    task.name = name
    task.description = description
    task.status = "assigned" if status == '' else status.lower()
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
    
    task.delete()

    return jsonify({"status": "success", "message": "Task deleted successfully."})


@task_bp.get('/getSingle')
def getSingletask():
    
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    task = Task.objects(id=id).first()
    if not task:
        return jsonify({"status": "error", "message": "Task not found."})
    
    actual_data = {
        "id": task.id,
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
    
    start = int(request.args.get('start', 0))  # Pagination Start
    length = int(request.args.get('length', 10))  # Pagination Limit
    
    # Search keyword
    search_value = request.args.get('search[value]', '').strip()
    
    # Sorting
    order_column_index = int(request.args.get('order[0][column]', 0))  # Column index
    order_direction = request.args.get('order[0][dir]', 'asc')  # Sort direction: asc or desc
    
    # Map column index to field names
    columns_map = {
        0: None,  # Default no sorting
        1: 'name',
        2: 'description',
        3: 'status',
        4: 'user',
        5: 'addedTime',
        6: 'updatedTime'
    }
    
    # Get sorting column
    order_column = columns_map.get(order_column_index)
    order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column
    
    task_query = Task.objects()

    # Apply search filter
    if search_value:
        task_query = task_query.filter(
            Q(name__icontains=search_value) |
            Q(description__icontains=search_value) |
            Q(status__icontains=search_value) | 
            Q(user__icontains=search_value) 
        )
    
    # Apply date range filter
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    today = request.args.get('today', 'false').lower() == 'true'
    
    if today:
        task_query = task_query.filter(
            added_time__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
    elif start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        task_query = task_query.filter(added_time__gte=start_date, added_time__lt=end_date)
    
    # Apply sorting
    if order_column:
        task_query = task_query.order_by(order_by)
    
    # Get total count before pagination
    total_records = task_query.count()
    
    # Apply pagination
    task = task_query.skip(start).limit(length)

    
    tasks = Task.objects()

    actual_data = []


    for task in tasks:

        data = {
            "id": task.id,
            "name":task.name,       
            "description":task.description,
            "status":task.status,
            "user": task.assignedTo.name if task.assignedTo else None,
            "addedTime":task.addedTime,
            "updatedTime":task.updatedTime
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "Task Retrieved Successfully", "data": actual_data, "recordsTotal": total_records, "recordsFiltered": total_records})


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
        return jsonify({"status":"error","message":"User not found"})

    for task in taskList:
        task = Task.objects(id=task).first()
        if not task:
            return jsonify({"status":"error","message":"Task not found"})          
        
        task.assignedTo = user
    
    task.save()

    return jsonify({"status":"success","message":"Task Assigned Successfully"})

@task_bp.get('/getAllNames')
def getAllNames():
    
    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    isPage = request.args.get("isPage")

    if isPage:
        tasks = Task.objects(assignedTo=current_user["id"])
    else:
        tasks= Task.objects()

    actual_data = []

    for task in tasks:
        data = {
            "id": task.id,
            "name":task.name,
            "description": task.description,
            "status": task.status     
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "Task Retrieved Successfully", "data": actual_data})
