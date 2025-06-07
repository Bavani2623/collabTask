from . import auth_bp
from flask import request, jsonify, session, redirect
from models import User

@auth_bp.post('/register')
def register():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    mobileNumber = data.get('number')
    

    if name == "" or email=="" or password=="" or mobileNumber=="":
         return jsonify({"status":"error", "message":"All data is required!"})
        
   
    if len(password)>4 and len(password)<8:
        user = User(
            name = name,
            email = email,
            password = password,
            mobileNumber = mobileNumber
        )

        user.save()
    else:
        return jsonify({"status":"error", "message":"password should be greater than 4 and less than 8"})
    
    return jsonify({"status":"success", "message":"User Register Successfully"})  




@auth_bp.post('/login')
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.objects(email=email).first()
    if not user:
        return jsonify({"status": "error", "message": "User not registered. Please Register to continue."})
    
    if user.password != password:
        return jsonify({"status": "error", "message": "User is registered but password is not matched"})
    
    userInfo = {
        "name": user.name,
        "email": user.email,
        "id": user.id
    }

    session["user"] = userInfo

    return jsonify({"status": "success", "message": "User Login Successfully"})


@auth_bp.get("/logout")
def logout():
    current_user = session.get("user")

    if current_user:
        session.clear()
        return redirect('/login')
    else:
        return jsonify({"status": "error", "message": "User is not login, please login to continue."})
    