from flask import request, jsonify
import os 
from app.utils.jwt_handler import get_user_id_from_token
from werkzeug.utils import secure_filename
from app.models.user import get_user_by_id
from app.models.course import (
    create_course_with_materials,
    update_course_with_materials,
    delete_course,
    get_course_for_edit,
    get_course_details_by_id,
    course_title_exists
)

#  Check admin role
def is_admin(user_id):
    user = get_user_by_id(user_id)
    return user and user.get("role_id") == 1


# ADD COURSE
def add_course():
    data = request.form
    pdf = request.files.get("pdf")

    title = data.get("title")
    description = data.get("description")
    cat_id = data.get("cat_id")
    diff_id = data.get("diff_id")
    created_by = data.get("created_by")

    if not title or not description or not cat_id or not diff_id or not created_by:
        return jsonify({"message": "Missing required course fields"}), 400

    content_url = data.get("content_url")

    if pdf:
        upload_folder = "uploads/materials"
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(pdf.filename)
        file_path = os.path.join(upload_folder, filename)
        pdf.save(file_path)

        content_url = file_path

    material = {
        "title": data.get("material_title"),
        "m_id": 1,
        "content_url": content_url,
        "content_text": data.get("content_text"),
        "order_index": data.get("order_index", 1)
    }

    if not material.get("title"):
        return jsonify({"message": "Material title is required"}), 400

    existing_course = course_title_exists(title)

    if existing_course:
        return jsonify({"message": "Course title already exists"}), 409

    course_id = create_course_with_materials(
        title,
        description,
        cat_id,
        diff_id,
        created_by,
        [material]
    )

    return jsonify({
        "message": "Course created successfully",
        "course_id": course_id
    }), 201


#  EDIT COURSE
def edit_course(course_id):
    user_id = get_user_id_from_token()

    if not user_id or not is_admin(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    cat_id = data.get("cat_id")
    diff_id = data.get("diff_id")
    materials = data.get("materials", [])

    if not title or not description or not cat_id or not diff_id:
        return jsonify({"error": "Missing required fields"}), 400

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


#  DELETE COURSE
def remove_course(course_id):
    user_id = get_user_id_from_token()

    if not user_id or not is_admin(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    delete_course(course_id)

    return jsonify({
        "message": "Course deleted successfully"
    }), 200


#  VIEW COURSE
def get_course(course_id):
    user_id = get_user_id_from_token()

    if not user_id or not is_admin(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    course = get_course_details_by_id(course_id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "course": course
    }), 200


#  LOAD COURSE FOR EDIT
def get_course_edit(course_id):
    user_id = get_user_id_from_token()

    if not user_id or not is_admin(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    course = get_course_for_edit(course_id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "course": course
    }), 200