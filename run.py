from flask import Flask
from app.routes.login import login
from app.routes.signup import signup

app = Flask(__name__)

app.add_url_rule("/login", "login", login, methods=["POST"])
app.add_url_rule("/signup", "signup", signup, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)