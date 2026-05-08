from flask import jsonify
from app.models.learning import get_learning_page_data


def learning_page(course_id, lesson_id):
    data = get_learning_page_data(course_id, lesson_id)

    if not data:
        return jsonify({
            "error": "Learning page data not found"
        }), 404

    return jsonify({
        "message": "Learning page loaded successfully",
        "data": data
    }), 200