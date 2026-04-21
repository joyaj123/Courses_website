from flask import Flask
from app.routes.signup import signup
from app.routes.login import login
from app.routes.courses import catalog, enroll
from app.models.user import get_db_connection



def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
     return "Hello World!"
    
    @app.route("/test-db")
    def test_db():
     try:
        conn = get_db_connection()
        return "Database connected successfully!"
     except Exception as e:
        return f"Error: {e}"
    
    

    app.add_url_rule("/signup", view_func=signup, methods=["POST"])
    app.add_url_rule("/login",  view_func=login,  methods=["POST"])
    app.add_url_rule("/courses",        view_func=catalog,  methods=["GET"])
    app.add_url_rule("/courses/enroll", view_func=enroll,   methods=["POST"])
    
    return app 