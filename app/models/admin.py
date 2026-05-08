from app.config.db import get_db_connection

def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Count users
        cursor.execute("SELECT COUNT(*) AS total_users FROM Users")
        users = cursor.fetchone()["total_users"]

        # Count courses
        cursor.execute("SELECT COUNT(*) AS total_courses FROM Courses")
        courses = cursor.fetchone()["total_courses"]

        # Count categories
        cursor.execute("SELECT COUNT(*) AS total_categories FROM Category")
        categories = cursor.fetchone()["total_categories"]

        return {
            "total_users": users,
            "total_courses": courses,
            "total_categories": categories
        }

    finally:
        cursor.close()
        conn.close()
    
    