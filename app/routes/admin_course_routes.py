from flask import request, jsonify
from app.utils.jwt_handler import get_user_id_from_token
from app.models.user import get_user_by_id
from app.models.course import (
    create_course_with_materials,
    update_course_with_materials,
    delete_course,
    get_course_for_edit,
    get_course_details_by_id
)

#  Check admin role
def is_admin(user_id):
    user = get_user_by_id(user_id)
    return user and user.get("role_id") == 1


# ADD COURSE
def add_course():
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

    course_id = create_course_with_materials(
        title,
        description,
        cat_id,
        diff_id,
        user_id,
        materials
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