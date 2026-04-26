from flask import jsonify
from app.utils.jwt_handler import get_user_id_from_token
from app.models.course import get_user_enrolled_courses
from app.models.course import get_categories_with_course_count


def get_my_courses():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "Invalid or missing token"}), 401

    courses = get_user_enrolled_courses(user_id)

    return jsonify({
        "message": "Enrolled courses fetched successfully",
        "courses": courses
    }), 200



def get_categories():
    categories = get_categories_with_course_count()

    return jsonify(categories), 200