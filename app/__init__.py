from flask import Flask
from app.routes.signup import signup
from app.routes.login import login
from app.models.user import get_db_connection
from app.routes.user_routes import get_me 
from app.routes.courses_routes import get_my_courses



def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
     return "Hello World!"
    
    @app.route("/test-db")
    def test_db():
     try:
        conn = get_db_connection()
        conn.close()
        
        return "Database connected successfully!"
     except Exception as e:
        return f"Error: {e}"
    
    

    app.add_url_rule("/signup", view_func=signup, methods=["POST"])
    app.add_url_rule("/login", view_func=login, methods=["POST"])
    app.add_url_rule("/me", view_func=get_me, methods=["GET"])
    app.add_url_rule("/my-courses", view_func=get_my_courses, methods=["GET"])


    
    return app 