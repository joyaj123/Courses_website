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