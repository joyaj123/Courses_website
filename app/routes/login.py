from flask import request, jsonify
from app.models.user import verify_user
from app.utils.jwt_handler import generate_token


def login():
    data = request.get_json(force=True)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = verify_user(email, password)

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user["user_id"])

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "email": user["email"],
            "role_id": user["role_id"]
        }
    }), 200