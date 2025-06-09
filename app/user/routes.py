from flask import jsonify, session, request
from . import user_bp
from models import User
from datetime import datetime

@user_bp.post('/add')
def addUser():

    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    mobileNumber = data.get('mobileNumber')

    if name == "" or email=="" or password=="" or mobileNumber=="":
         return jsonify({"status":"error","message":"all data is required!"})
    
    user = User(
        name = name,
        email = email,
        password = password,
        mobileNumber = mobileNumber
    )

    user.save()

    return jsonify({"status": "success", "message": "User Added successfully."})


@user_bp.put('/update')
def updateUser():

    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    user = User.objects(id=id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found."})
    
    data = request.get_json()

    name = data.get('name')
    password = data.get('password')
    mobileNumber = data.get('mobileNumber')

    if name == "" or password=="" or mobileNumber=="":
        return jsonify({"status":"error","message":"all data is required!"})
    
    user.name = name
    user.password = password
    user.mobileNumber = mobileNumber
    user.updatedTime = datetime.now()

    user.save()

    return jsonify({"status": "success", "message": "User Updated successfully."})

@user_bp.delete('/delete')
def deleteUser():

    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    user = User.objects(id=id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found."})
    
    user.delete()

    return jsonify({"status": "success", "message": "User deleted successfully."})


@user_bp.get('/getSingle')
def getSingleUser():
    
    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})

    id = request.args.get("id")

    if not id:
        return jsonify({"status": "error", "message": "Id not found"})
    
    user = User.objects(id=id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found."})
    
    actual_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "mobileNumber": user.mobileNumber,
        "addedTime": user.addedTime,
        "updatedTime": user.updatedTime
    }

    return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": actual_data})

@user_bp.get('/getMany')
def getMany():
    
    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    users = User.objects()

    actual_data = []

    for user in users:
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "mobileNumber": user.mobileNumber,
            "addedTime": user.addedTime,
            "updatedTime": user.updatedTime
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": actual_data})

@user_bp.get('/getAllNames')
def getAllNames():
    
    current_user = session["user"]

    if not current_user:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
    
    users = User.objects()

    actual_data = []

    for user in users:
        data = {
            "id": user.id,
            "name": user.name
        }

        actual_data.append(data)

    return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": actual_data})