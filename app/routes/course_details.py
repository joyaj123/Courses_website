from flask import render_template
from app.models.course import get_course_details_by_id


def course_details(course_id):
    course = get_course_details_by_id(course_id)

    if not course:
        return render_template(
            "course_details.html",
            course=None,
            error="Course not found"
        )

    return render_template(
        "course_details.html",
        course=course
    )


def course_material(course_id, material_id):
    course = get_course_details_by_id(course_id)

    if not course:
        return render_template(
            "course_material.html",
            course=None,
            material=None,
            error="Course not found"
        )

    selected_material = None

    for material in course.get("materials", []):
        if str(material.get("material_id")) == str(material_id):
            selected_material = material
            break

    if not selected_material:
        return render_template(
            "course_material.html",
            course=course,
            material=None,
            error="Material not found"
        )

    return render_template(
        "course_material.html",
        course=course,
        material=selected_material,
        error=None
    )