from app.models.user import get_db_connection

def get_all_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.course_id,
            c.title,
            c.description,
            cat.description  AS category,
            diff.level       AS difficulty
        FROM Courses c
        JOIN Category   cat  ON c.cat_id  = cat.cat_id
        JOIN Difficulty diff ON c.diff_id = diff.diff_id
    """)

    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses


def enroll_user(user_id, course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if already enrolled
    cursor.execute("""
        SELECT * FROM Enrollments
        WHERE user_id = %s AND course_id = %s
    """, (user_id, course_id))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conn.close()
        return "already_enrolled"

    # Get active status id
    cursor.execute("SELECT s_id FROM Status WHERE description = 'active'")
    status = cursor.fetchone()

    cursor.execute("""
        INSERT INTO Enrollments (user_id, course_id, s_id)
        VALUES (%s, %s, %s)
    """, (user_id, course_id, status["s_id"]))

    conn.commit()
    cursor.close()
    conn.close()
    return "enrolled"