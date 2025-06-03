from . import main_bp
from flask import render_template, request, jsonify

@main_bp.get('/')
def home():
    return render_template("dashboard.html")

@main_bp.get('/<page>')
def load_page(page):
    return render_template(f"{page}.html")    

              
              