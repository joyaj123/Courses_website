from flask import request, jsonify
from app.models.user import get_user_by_email
from app.utils.jwt_handler import generate_token

def login():
    data = request.get_json()

    email    = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result = get_user_by_email(email, password)

    if result == "not_found":
        return jsonify({"error": "No account found with that email"}), 404

    if result == "wrong_password":
        return jsonify({"error": "Incorrect password"}), 401

    token = generate_token(result["user_id"])
    return jsonify({
        "message": "Login successful",
        "token": token,
        "role": result["role"]
    }), 200