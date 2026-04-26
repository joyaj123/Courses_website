import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


#  Connect to DB
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Elinka81@",
        database="cs_learning_platform"
    )

def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user exists
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return "exists"

    #  GET learner role_id
    cursor.execute("SELECT role_id FROM Role WHERE type = %s", ("learner",))
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
    INSERT INTO Users (username, email, password_hash, role_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (username, email, hashed_password, role_id))

    conn.commit()
    user_id = cursor.lastrowid  # 🔥 IMPORTANT

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
        SELECT user_id, username, email, role, created_at, updated_at
        FROM users
        WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
