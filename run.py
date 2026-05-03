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
from app.routes.admin_course_routes import (
    add_course,
    edit_course,
    remove_course,
    get_course,
    get_course_edit
)

app.add_url_rule('/admin/course', view_func=add_course, methods=['POST'])

app.add_url_rule('/admin/course/<int:course_id>', view_func=edit_course, methods=['PUT'])

app.add_url_rule('/admin/course/<int:course_id>', view_func=remove_course, methods=['DELETE'])

app.add_url_rule('/admin/course/<int:course_id>', view_func=get_course, methods=['GET'])

app.add_url_rule('/admin/course/edit/<int:course_id>', view_func=get_course_edit, methods=['GET'])


if __name__ == "__main__":
    app.run(debug=True)