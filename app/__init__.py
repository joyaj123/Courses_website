from flask import Flask, render_template

# Auth routes
from app.routes.login import login
from app.routes.signup import signup
from app.routes.user_routes import get_me

# Learning routes
from app.routes.learning_routes import learning_page

# Course routes
from app.routes.courses_routes import (
    get_my_courses,
    get_categories,
    get_courses_dashboardadmin,
    delete_course
)

# Admin course routes
from app.routes.admin_course_routes import (
    add_course,
    edit_course,
    remove_course,
    get_course,
    get_course_edit
)

# Course details
from app.routes.course_details import course_details


def create_app():
    app = Flask(__name__)


    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/admin/courses/create")
    def create_course_page():
        return render_template("admin_create_course.html")

    @app.route("/admin/manage-courses")
    def create_manage_course_page():
        return render_template("manage_courses_admin.html")

    @app.route("/course-catalog")
    def course_catalog_page():

      return render_template("course_catalog.html")
    
    @app.route('/admin-dashboard')
    def admin_dashboard():
        return render_template("admin_dashboard.html")
    
    @app.route('/learner-dashboard')
    def learner_dashboard():
        return render_template("learner_dashboard.html")

    @app.route("/home")
    def home_page():
        return "<h1>Welcome Home</h1>"
        
    

        return render_template("course_catalog.html")
    
    @app.route("/signup-page")
    def signup_page():
        return render_template("signup.html")
    
    @app.route("/profile")
    def profile_page():
        return  render_template("profile.html")


    # AUTH API
    app.add_url_rule("/signup", view_func=signup, methods=["POST"])
    app.add_url_rule("/login", view_func=login, methods=["POST"])

    # USER API
    app.add_url_rule("/me", view_func=get_me, methods=["GET"])

    # COURSES API
    app.add_url_rule("/my-courses", view_func=get_my_courses, methods=["GET"])
    app.add_url_rule("/categories", view_func=get_categories, methods=["GET"])
    app.add_url_rule("/course-manage", view_func=get_courses_dashboardadmin, methods=["GET"])

    # COURSE DETAILS / LEARNING
    app.add_url_rule("/courses/<int:course_id>/details", view_func=course_details, methods=["GET"])

    app.add_url_rule(
        "/courses/<int:course_id>/learning/<int:lesson_id>",
        view_func=learning_page,
        methods=["GET"]
    )

    # ADMIN COURSE API
    app.add_url_rule("/add-courses", view_func=add_course, methods=["POST"])
    app.add_url_rule("/courses/<int:course_id>", view_func=get_course_edit, methods=["GET"])
    app.add_url_rule("/courses/<int:course_id>", view_func=edit_course, methods=["PUT"])
    app.add_url_rule("/courses/<int:course_id>", view_func=delete_course, methods=["DELETE"])

    return app