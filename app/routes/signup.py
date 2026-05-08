from flask import request, jsonify
from app.models.user import create_user
from app.utils.jwt_handler import generate_token
from app.utils.validators import is_strong_password

def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    
    if len(password) < 6:
      return jsonify({"error": "Password must be at least 6 characters"}), 400
    

    is_valid, message = is_strong_password(password)

    if not is_valid:
      return jsonify({"error": message}), 400


    result = create_user(username, email, password)

    if result == "email_exists":
        return jsonify({"error": "Email already exists"}), 400

    if result == "username_exists":
        return jsonify({"error": "Username already exists"}), 400

    if result == "no_role":
        return jsonify({"error": "Learner role not found"}), 500

    token = generate_token(result)

    return jsonify({
        "message": "User created successfully",
        "token": token
    }), 201