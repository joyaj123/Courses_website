
from flask import jsonify
from app.models.course import get_course_details_by_id


def course_details(course_id):
    course = get_course_details_by_id(course_id)

    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify({
        "message": "Course details loaded successfully",
        "course": course
    }), 200