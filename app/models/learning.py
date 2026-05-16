from app.config.db import get_db_connection


def get_learning_page_data(course_id, lesson_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT course_id, title, description
        FROM courses
        WHERE course_id = %s
    """, (course_id,))
    course = cursor.fetchone()

    if not course:
        cursor.close()
        conn.close()
        return None

    cursor.execute("""
        SELECT
            material_id,
            title,
            content_url,
            content_text,
            order_index
        FROM course_materials
        WHERE course_id = %s
        AND material_id = %s
    """, (course_id, lesson_id))
    current_lesson = cursor.fetchone()

    if not current_lesson:
        cursor.close()
        conn.close()
        return None

    cursor.execute("""
        SELECT
            material_id,
            title,
            order_index
        FROM course_materials
        WHERE course_id = %s
        ORDER BY order_index ASC
    """, (course_id,))
    lessons = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "course": {
            "id": course["course_id"],
            "title": course["title"],
            "description": course["description"],
            "progress": 68
        },
        "current_lesson": {
            "id": current_lesson["material_id"],
            "module_number": 4,
            "lesson_number": current_lesson["order_index"],
            "title": current_lesson["title"],
            "duration": "45 minutes",
            "level": "Advanced Mastery",
            "content_url": current_lesson["content_url"],
            "content_text": current_lesson["content_text"]
        },
        "lessons": [
            {
                "id": lesson["material_id"],
                "title": lesson["title"],
                "order_index": lesson["order_index"],
                "is_active": lesson["material_id"] == lesson_id
            }
            for lesson in lessons
        ]
    }

from app.config.db import get_db_connection


def enroll_user_in_course(user_id, course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Check if course exists
        cursor.execute("""
            SELECT course_id
            FROM Courses
            WHERE course_id = %s
        """, (course_id,))

        course = cursor.fetchone()

        if not course:
            return {
                "success": False,
                "message": "Course not found"
            }

        # Check if already enrolled
        cursor.execute("""
            SELECT enrol_id
            FROM Enrollments
            WHERE user_id = %s AND course_id = %s
        """, (user_id, course_id))

        existing = cursor.fetchone()

        if existing:
            return {
                "success": False,
                "message": "Already enrolled"
            }

        # s_id = 3 means enrolled
        cursor.execute("""
            INSERT INTO Enrollments (user_id, course_id, s_id)
            VALUES (%s, %s, %s)
        """, (user_id, course_id, 3))

        conn.commit()

        return {
            "success": True,
            "message": "Enrolled successfully"
        }

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": str(e)
        }

    finally:
        cursor.close()
        conn.close()


def is_user_enrolled(user_id, course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT enrol_id
            FROM Enrollments
            WHERE user_id = %s AND course_id = %s
        """, (user_id, course_id))

        return cursor.fetchone() is not None

    finally:
        cursor.close()
        conn.close()


def get_user_enrolled_courses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                c.course_id,
                c.title,
                c.description,
                cat.description AS category,
                d.level AS difficulty,
                e.enrolled_at
            FROM Enrollments e
            JOIN Courses c ON e.course_id = c.course_id
            JOIN Category cat ON c.cat_id = cat.cat_id
            JOIN Difficulty d ON c.diff_id = d.diff_id
            WHERE e.user_id = %s
            ORDER BY e.enrolled_at DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()