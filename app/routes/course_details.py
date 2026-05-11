from flask import render_template, jsonify
from app.models.course import get_course_details_by_id


def course_details(course_id):
    course = get_course_details_by_id(course_id)

    if not course:
        return render_template("course_details.html", course=None, error="Course not found")

    return render_template("course_details.html", course=course)