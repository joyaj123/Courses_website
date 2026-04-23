import mysql.connector
from werkzeug.security import generate_password_hash

#  Connect to DB
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="project_management"
    )

def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return "exists"

    #  GET learner role_id
    cursor.execute("SELECT role_id FROM role WHERE type = %s", ("learner",))
    role = cursor.fetchone()

    if not role:
        cursor.close()
        conn.close()
        return "no_role"

    role_id = role["role_id"]

    # Hash password
    hashed_password = generate_password_hash(password)

    # Insert user WITH role_id
    query = """
    INSERT INTO users (username, email, password_hash, role_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (username, email, hashed_password, role_id))

    conn.commit()
    user_id = cursor.lastrowid  # 🔥 IMPORTANT

    cursor.close()
    conn.close()

    return "created"


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT user_id, username, email, role, created_at, updated_at
        FROM users
        WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user