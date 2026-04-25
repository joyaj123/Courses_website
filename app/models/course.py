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