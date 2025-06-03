from . import auth_bp
from flask import request, jsonify
from models import User

@auth_bp.post('/register')
def register():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    mobileNumber = data.get('number')
    

    if name == "" or email=="" or password=="" or mobileNumber=="":
         return jsonify({"status":"error","message":"all data is required!"})
        
   
    if len(password)>4 and len(password)<8:
        user = User(
            name = name,
            email = email,
            password = password,
            mobileNumber = mobileNumber
        )

        user.save()
    else:
        return jsonify({"status":"error","message":"password should be greater than 4 and less than 8"})
    
    return jsonify({"message":"User register successfully"})
   
          


       
    