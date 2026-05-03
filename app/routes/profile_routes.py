from flask import request, jsonify
from app.models.profile import get_user_profile, update_user_profile
from app.utils.jwt_handler import get_user_id_from_token


def get_profile():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "Login required"}), 401

    user = get_user_profile(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "Profile loaded successfully",
        "user": user
    }), 200


def update_profile():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()

    username        = data.get("username")
    email           = data.get("email")
    current_password = data.get("current_password")
    new_password     = data.get("new_password")

    # Validate required fields
    if not username or not email or not current_password:
        return jsonify({"error": "Username, email and current password are required"}), 400

    # Validate email format
    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email format"}), 400

    # Validate new password length if provided
    if new_password and len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400

    result = update_user_profile(
        user_id,
        username,
        email,
        current_password,
        new_password
    )

    if result == "not_found":
        return jsonify({"error": "User not found"}), 404

    if result == "wrong_password":
        return jsonify({"error": "Current password is incorrect"}), 401

    if result == "email_taken":
        return jsonify({"error": "Email is already in use"}), 409

    if result == "username_taken":
        return jsonify({"error": "Username is already taken"}), 409

    return jsonify({
        "message": "Profile updated successfully"
    }), 200