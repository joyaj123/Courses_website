from flask import render_template
from app.models.learning import get_learning_page_data


def learning_page(course_id, lesson_id):
    data = get_learning_page_data(course_id, lesson_id)

    if not data:
        return render_template("lesson_player.html", data=None, error="Lesson not found")

    return render_template("lesson_player.html", data=data)



from flask import render_template, jsonify
from app.models.learning import (
    get_learning_page_data,
    enroll_user_in_course,
    is_user_enrolled,
    get_user_enrolled_courses
)
from app.utils.jwt_handler import get_user_id_from_token


def learning_page(course_id, lesson_id):
    data = get_learning_page_data(course_id, lesson_id)

    if not data:
        return render_template("lesson_player.html", data=None, error="Lesson not found")

    return render_template("lesson_player.html", data=data)


def enroll_course(course_id):
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "You must login first"}), 401

    result = enroll_user_in_course(user_id, course_id)

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


def check_enrollment(course_id):
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"enrolled": False}), 200

    enrolled = is_user_enrolled(user_id, course_id)

    return jsonify({"enrolled": enrolled}), 200


def my_courses():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "You must login first"}), 401

    courses = get_user_enrolled_courses(user_id)

    return jsonify(courses), 200