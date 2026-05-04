from flask import Flask, render_template
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

    # PAGE ROUTES
    @app.route("/")
    def login_page():
        return render_template("login.html")
    

    @app.route("/admin/courses/create")
    def create_course_page():
      return render_template("admin_create_course.html")

    @app.route("/home")
    def home_page():
        return "<h1>Welcome Home</h1>"

    # AUTH API ROUTES
    app.add_url_rule("/signup", view_func=signup, methods=["POST"])
    app.add_url_rule("/login", view_func=login, methods=["POST"])

    # USER API ROUTES
    app.add_url_rule("/me", view_func=get_me, methods=["GET"])

    # COURSE API ROUTES
    app.add_url_rule("/my-courses", view_func=get_my_courses, methods=["GET"])
    app.add_url_rule("/categories", view_func=get_categories, methods=["GET"])
    app.add_url_rule("/add-courses", view_func=add_course, methods=["POST"])

    app.add_url_rule("/courses/<int:course_id>", view_func=get_course_edit, methods=["GET"])
    app.add_url_rule("/courses/<int:course_id>", view_func=edit_course, methods=["PUT"])

    app.add_url_rule("/courses/<int:course_id>/details", view_func=course_details, methods=["GET"])

    app.add_url_rule(
        "/courses/<int:course_id>/learning/<int:lesson_id>",
        view_func=learning_page,
        methods=["GET"]
    )

    return app