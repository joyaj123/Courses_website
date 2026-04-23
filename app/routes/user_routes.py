from flask import jsonify
from app.utils.jwt_handler import get_user_id_from_token
from app.models.user import get_user_by_id


def get_me():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "Invalid or missing token"}), 401

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200 