import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Elinka81@", 
        database="cs_learning_platform"
    )


def get_course_details_by_id(course_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get course information with category and difficulty names
        cursor.execute(
            """
            SELECT
                c.course_id,
                c.title,
                c.description,
                c.cat_id,
                cat.description AS category,
                c.diff_id,
                d.level AS difficulty,
                c.created_by,
                u.username AS created_by_username,
                c.created_at,
                c.updated_at
            FROM Courses c
            JOIN Category cat ON c.cat_id = cat.cat_id
            JOIN Difficulty d ON c.diff_id = d.diff_id
            JOIN Users u ON c.created_by = u.user_id
            WHERE c.course_id = %s
            """,
            (course_id,)
        )

        course = cursor.fetchone()

        if not course:
            return None

        # Get course materials with material type name
        cursor.execute(
            """
            SELECT
                cm.material_id,
                cm.course_id,
                cm.title,
                cm.m_id,
                mt.description AS material_type,
                cm.content_url,
                cm.content_text,
                cm.order_index,
                cm.created_at
            FROM Course_Materials cm
            JOIN Material_Type mt ON cm.m_id = mt.m_id
            WHERE cm.course_id = %s
            ORDER BY cm.order_index ASC
            """,
            (course_id,)
        )

        materials = cursor.fetchall()
        course["materials"] = materials

        return course

    finally:
        cursor.close()
        connection.close()
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



