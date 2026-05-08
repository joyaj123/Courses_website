import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.db import get_db_connection



def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # Check if email or username already exists
    cursor.execute(
        "SELECT * FROM Users WHERE email = %s OR username = %s",
        (email, username)
    )
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()

        if existing_user["email"] == email:
            return "email_exists"

        if existing_user["username"] == username:
            return "username_exists"

    # Get learner role_id
    cursor.execute("SELECT role_id FROM Role WHERE type = %s", ("learner",))
    role = cursor.fetchone()

    if not role:
        cursor.close()
        conn.close()
        return "no_role"

    role_id = role["role_id"]

    # Hash password
    hashed_password = generate_password_hash(password)

    # Insert user
    query = """
        INSERT INTO Users (username, email, password_hash, role_id)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (username, email, hashed_password, role_id))
    conn.commit()

    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return user_id

#retrieves a user from the database using email
def get_user_by_email(email):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)

    query = "SELECT * FROM Users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
    
#verifies user login 
def verify_user(email,password):
    user=get_user_by_email(email)

    if not user:
        return None
    if check_password_hash(user["password_hash"],password):
        return user
    return None


    return "created"


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT user_id, username, email, role_id, created_at, updated_at
        FROM users
        WHERE user_id = %s
        SELECT 
            u.user_id,
            u.username,
            u.email,
            u.role_id,
            r.type AS role
        FROM Users u
        JOIN Role r ON u.role_id = r.role_id
        WHERE u.user_id = %s
    """
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
