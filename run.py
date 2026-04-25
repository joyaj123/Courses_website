from flask import Flask
from app.routes.login import login
from app.routes.signup import signup
from app.routes.course_details import course_details

app = Flask(__name__)

app.add_url_rule("/login", "login", login, methods=["POST"])
app.add_url_rule("/signup", "signup", signup, methods=["POST"])

#course_details route
app.add_url_rule(
    "/courses/<int:course_id>",
    "course_details",
    course_details,
    methods=["GET"]
)

if __name__ == "__main__":
    app.run(debug=True)