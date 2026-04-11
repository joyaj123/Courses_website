from flask import request, jsonify
from app.models.user import create_user
from app.utils.jwt_handler import generate_token


def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    result = create_user(username, email, password)

    if result == "exists":
        return jsonify({"error": "User already exists"}), 400

    
    token = generate_token(result)

    return jsonify({
        "message": "User created successfully",
        "token": token
    }), 201