from flask import Flask
from app.routes.login import login
from app.routes.signup import signup
from app.routes.user_routes import get_me
from app.routes.learning_routes import learning_page
from app.routes.courses_routes import (
    get_my_courses,
    get_categories,
    add_course,
    get_course_edit,
    edit_course
)
from app.routes.course_details import course_details


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello World!"

    # AUTH
    app.add_url_rule("/signup", view_func=signup, methods=["POST"])
    app.add_url_rule("/login", view_func=login, methods=["POST"])

    # USER
    app.add_url_rule("/me", view_func=get_me, methods=["GET"])

    # COURSES
    app.add_url_rule("/my-courses", view_func=get_my_courses, methods=["GET"])
    app.add_url_rule("/categories", view_func=get_categories, methods=["GET"])
    app.add_url_rule("/courses", view_func=add_course, methods=["POST"])

    # COURSE EDIT
    app.add_url_rule("/courses/<int:course_id>", view_func=get_course_edit, methods=["GET"])
    app.add_url_rule("/courses/<int:course_id>", view_func=edit_course, methods=["PUT"])

    # COURSE DETAILS
    app.add_url_rule("/courses/<int:course_id>/details", view_func=course_details, methods=["GET"])

    #learning
    app.add_url_rule(
    "/courses/<int:course_id>/learning/<int:lesson_id>",
    view_func=learning_page,
    methods=["GET"]
)

    return app