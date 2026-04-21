import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

#  Connect to DB
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ritajones19@senoj21",
        database="cs_learning_platform"
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

    return user_id #fix/changed it so create_user return the actual user_id instead of the string "created"

def get_user_by_email(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.user_id, u.username, u.email, u.password_hash, r.type AS role
        FROM Users u
        JOIN Role r ON u.role_id = r.role_id
        WHERE u.email = %s
    """, (email,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return "not_found"

    if not check_password_hash(user["password_hash"], password):
        return "wrong_password"

    return user