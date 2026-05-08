from app.config.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                u.user_id,
                u.username,
                u.email,
                u.created_at,
                r.type AS role
            FROM Users u
            JOIN Role r ON u.role_id = r.role_id
            WHERE u.user_id = %s
        """, (user_id,))

        user = cursor.fetchone()
        return user

    finally:
        cursor.close()
        conn.close()


def update_user_profile(user_id, username, email, current_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get current user data to verify password
        cursor.execute("""
            SELECT * FROM Users WHERE user_id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return "not_found"

        # Always verify current password before making any changes
        if not check_password_hash(user["password_hash"], current_password):
            return "wrong_password"

        # Check if new email is taken by someone else
        if email != user["email"]:
            cursor.execute("""
                SELECT user_id FROM Users
                WHERE email = %s AND user_id != %s
            """, (email, user_id))

            if cursor.fetchone():
                return "email_taken"

        # Check if new username is taken by someone else
        if username != user["username"]:
            cursor.execute("""
                SELECT user_id FROM Users
                WHERE username = %s AND user_id != %s
            """, (username, user_id))

            if cursor.fetchone():
                return "username_taken"

        # If new password provided, hash it, otherwise keep the old one
        if new_password:
            password_hash = generate_password_hash(new_password)
        else:
            password_hash = user["password_hash"]

        cursor.execute("""
            UPDATE Users
            SET username = %s,
                email = %s,
                password_hash = %s
            WHERE user_id = %s
        """, (username, email, password_hash, user_id))

        conn.commit()
        return "updated"

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()