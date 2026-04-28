from app import create_app

# import routes
from app.routes.login import login
from app.routes.signup import signup
from app.routes.user_routes import get_me
from app.routes.courses_routes import get_my_courses, add_course
from app.routes.course_details import course_details
from app.routes.courses_routes import get_course_edit, edit_course

app = create_app()

# AUTH
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/signup", view_func=signup, methods=["POST"])

# USER
app.add_url_rule("/me", view_func=get_me, methods=["GET"])

# COURSES
app.add_url_rule("/my-courses", view_func=get_my_courses, methods=["GET"])
app.add_url_rule("/courses/<int:course_id>", view_func=course_details, methods=["GET"])

#ADMIN ROUTES
app.add_url_rule("/admnin/add-courses", view_func=add_course, methods=["POST"]) ####t to check when doing front end 
app.add_url_rule("/admin/courses/<int:course_id>", view_func=get_course_edit, methods=["GET"])
app.add_url_rule("/admin/courses/<int:course_id>", view_func=edit_course, methods=["PUT"])


if __name__ == "__main__":
    app.run(debug=True)