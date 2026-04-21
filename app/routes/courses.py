from flask import request, jsonify
from app.models.course import get_all_courses, enroll_user
from app.utils.jwt_handler import decode_token

def catalog():
    courses = get_all_courses()
    return jsonify({"courses": courses}), 200


def enroll():
    # Check authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Login required"}), 401

    token = auth_header.split(" ")[1]
    payload = decode_token(token)

    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 401

    data      = request.get_json()
    course_id = data.get("course_id")

    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    result = enroll_user(payload["user_id"], course_id)

    if result == "already_enrolled":
        return jsonify({"error": "You are already enrolled in this course"}), 400

    return jsonify({"message": "Successfully enrolled in course"}), 201