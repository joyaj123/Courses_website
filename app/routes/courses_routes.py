from flask import request, jsonify
import os
from werkzeug.utils import secure_filename

from app.utils.jwt_handler import get_user_id_from_token
from app.models.course import (
    get_user_enrolled_courses,
    get_categories_with_course_count,
    course_title_exists,
    create_course_with_materials,
    get_course_for_edit,
    update_course_with_materials
)


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




def add_course():
    data = request.form
    pdf = request.files.get("pdf")

    title = data.get("title")
    description = data.get("description")
    cat_id = data.get("cat_id")
    diff_id = data.get("diff_id")
    created_by = data.get("created_by")

    if not title or not description or not cat_id or not diff_id or not created_by:
        return jsonify({
            "message": "Missing required course fields"
        }), 400

    content_url = None

    if pdf:
        upload_folder = "uploads/materials"
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(pdf.filename)
        file_path = os.path.join(upload_folder, filename)

        pdf.save(file_path)
        content_url = file_path

    materials = [
        {
            "title": data.get("material_title"),
            "m_id": data.get("m_id"),
            "content_url": data.get("content_url"),
            "content_text": data.get("content_text"),
            "order_index": data.get("order_index", 1)
        }
    ]

    for material in materials:
        if not material.get("title") or not material.get("m_id"):
            return jsonify({
                "message": "Each material must have title and m_id"
            }), 400

    existing_course = course_title_exists(title)

    if existing_course:
        return jsonify({
            "message": "Course title already exists"
        }), 409

    course_id = create_course_with_materials(
        title,
        description,
        cat_id,
        diff_id,
        created_by,
        materials
    )

    return jsonify({
        "message": "Course created successfully",
        "course_id": course_id
    }), 201


def get_course_edit(course_id):
    course = get_course_for_edit(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    return jsonify({
        "message": "Course loaded successfully",
        "course": course
    }), 200



def edit_course(course_id):
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    cat_id = data.get("cat_id")
    diff_id = data.get("diff_id")
    materials = data.get("materials", [])

    if not title or not description or not cat_id or not diff_id:
        return jsonify({
            "message": "Missing required course fields"
        }), 400

    update_course_with_materials(
        course_id,
        title,
        description,
        cat_id,
        diff_id,
        materials
    )

    return jsonify({
        "message": "Course updated successfully"
    }), 200