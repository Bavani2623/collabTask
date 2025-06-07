from . import main_bp
from flask import render_template, jsonify, session

@main_bp.get('/')
def home():
    current_user = session.get("user")
    print(current_user)

    if current_user:
        return render_template("dashboard.html")    
    else:
        return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
              

@main_bp.get('/<page>')
def load_page(page):
    current_user = session.get("user")
    print(current_user)

    if current_user:
        return render_template(f"{page}.html")    
    else:
        if page == "login" or page == "register":
            return render_template(f"{page}.html")  
        
    return jsonify({"status": "error", "message": "User not login. Unauthorized Access!"})
              