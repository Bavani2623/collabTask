from flask import jsonify, session, request
from . import project_bp
from models import Project
from datetime import datetime, timedelta
from mongoengine import Q

@project_bp.post('/add')
def addProject():

    current_user = session.get("user")

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

    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    project = Project.objects(id=id).first()
    
    if not project:
        return jsonify({"status": "error", "message": "Project not found."})

    
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    
    
    project.name = name
    project.description = description
    project.updatedTime = datetime.now()

    project.save()

    return jsonify({"status": "success", "message": "Project  Updated successfully."})

@project_bp.delete('/delete')
def deleteProject():

    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    project = Project.objects(id=id).first()
    
    if not project:
        return jsonify({"status": "error", "message": "Project not found."})

    project.delete()

    return jsonify({"status": "success", "message": "Project deleted successfully."})


@project_bp.get('/getSingle')
def getSingleProject():
    
    current_user = session.get("user")

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    project = Project.objects(id=id).first()
    
    if not project:
        return jsonify({"status": "error", "message": "Project not found."})
    
    actual_data = {
        "id": project.id,
        "name":  project.name,
        "description":  project.description,
        "addedTime":  project.addedTime,
        "updatedTime":  project.updatedTime
    }

    return jsonify({"status": "success", "message": "Project Retrieved Successfully", "data": actual_data})

@project_bp.get('/getMany')
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
        3: 'addedTime',
        4: 'updatedTime'
    }
    
    # Get sorting column
    order_column = columns_map.get(order_column_index)
    order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column
    
    project_query = Project.objects()

    # Apply search filter
    if search_value:
        project_query = project_query.filter(
            Q(name__icontains=search_value) |
            Q(description__icontains=search_value)
        )
    
    # Apply date range filter
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    today = request.args.get('today', 'false').lower() == 'true'
    
    if today:
        project_query = project_query.filter(
            added_time__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
    elif start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        project_query = project_query.filter(added_time__gte=start_date, added_time__lt=end_date)
    
    # Apply sorting
    if order_column:
        project_query = project_query.order_by(order_by)
    
    # Get total count before pagination
    total_records = project_query.count()
    
    # Apply pagination
    projects = project_query.skip(start).limit(length)

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

    return jsonify({"status": "success", "message": "Project Retrieved Successfully", "data": actual_data, "recordsTotal": total_records, "recordsFiltered": total_records})