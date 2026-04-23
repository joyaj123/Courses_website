from app.models.user import get_db_connection

def get_user_enrolled_courses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            e.enrol_id,
            e.enrolled_at,
            s.description AS enrollment_status,

            c.course_id,
            c.title,
            c.description,
            c.created_at,
            c.updated_at,

            cat.description AS category,
            d.level AS difficulty,

            COUNT(cm.material_id) AS total_materials,
            MIN(cm.order_index) AS first_material_order
        FROM Enrollments e
        INNER JOIN Courses c
            ON e.course_id = c.course_id
        INNER JOIN Status s
            ON e.s_id = s.s_id
        INNER JOIN Category cat
            ON c.cat_id = cat.cat_id
        INNER JOIN Difficulty d
            ON c.diff_id = d.diff_id
        LEFT JOIN Course_Materials cm
            ON c.course_id = cm.course_id
        WHERE e.user_id = %s
        GROUP BY
            e.enrol_id,
            e.enrolled_at,
            s.description,
            c.course_id,
            c.title,
            c.description,
            c.created_at,
            c.updated_at,
            cat.description,
            d.level
        ORDER BY e.enrolled_at DESC
    """

    cursor.execute(query, (user_id,))
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses


def get_categories_with_course_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            cat.cat_id,
            cat.description AS category_name,
            COUNT(c.course_id) AS total_courses
        FROM Category cat
        LEFT JOIN Courses c
            ON cat.cat_id = c.cat_id
        GROUP BY cat.cat_id, cat.description
    """

    cursor.execute(query)
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return categories



