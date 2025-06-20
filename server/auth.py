from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from models import User
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print("Received data:", request.data)
    print("Parsed JSON:", request.get_json())

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=username)   # Set only username
    user.set_password(password)      # Set password_hash using the method
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        token = create_access_token(identity=str(user.id))  # <-- convert to string
        return jsonify(access_token=token), 200
    
    return jsonify({"error":"invalid user"}), 401



@auth_bp.route('/dashboard', methods=["GET"])
@jwt_required()
def get_dashboard():
    current_user = get_jwt_identity()
    # You must define how to fetch user data here:
    user = User.query.get(current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": f"Welcome {user.username} to your dashboard!",
        "user_id": user.id,
        "username": user.username
    }), 200