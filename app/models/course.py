from app.config.db import get_db_connection



def get_course_details_by_id(course_id):
    connection = get_db_connection()
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



def course_title_exists(title):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT course_id
        FROM Courses
        WHERE title = %s
    """, (title,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def create_course_with_materials(title, description, cat_id, diff_id, created_by, materials):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            INSERT INTO Courses (title, description, cat_id, diff_id, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, cat_id, diff_id, created_by))

        course_id = cursor.lastrowid

        for material in materials:
            cursor.execute("""
                INSERT INTO Course_Materials
                (course_id, title, m_id, content_url, content_text, order_index)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                course_id,
                material.get("title"),
                material.get("m_id"),
                material.get("content_url"),
                material.get("content_text"),
                material.get("order_index", 0)
            ))

        conn.commit()
        return course_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()


#get the course info anf course matirial 
def get_course_for_edit(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                course_id,
                title,
                description,
                cat_id,
                diff_id,
                created_by
            FROM Courses
            WHERE course_id = %s
        """, (course_id,))

        course = cursor.fetchone()

        if not course:
            return None

        cursor.execute("""
            SELECT
                material_id,
                title,
                m_id,
                content_url,
                content_text,
                order_index
            FROM Course_Materials
            WHERE course_id = %s
            ORDER BY order_index ASC
        """, (course_id,))

        course["materials"] = cursor.fetchall()

        return course

    finally:
        cursor.close()
        conn.close()



def update_course_with_materials(course_id, title, description, cat_id, diff_id, materials):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            UPDATE Courses
            SET title = %s,
                description = %s,
                cat_id = %s,
                diff_id = %s
            WHERE course_id = %s
        """, (title, description, cat_id, diff_id, course_id))

        for material in materials:
            material_id = material.get("material_id")

            if material_id:
                cursor.execute("""
                    UPDATE Course_Materials
                    SET title = %s,
                        m_id = %s,
                        content_url = %s,
                        content_text = %s,
                        order_index = %s
                    WHERE material_id = %s AND course_id = %s
                """, (
                    material.get("title"),
                    material.get("m_id"),
                    material.get("content_url"),
                    material.get("content_text"),
                    material.get("order_index", 0),
                    material_id,
                    course_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO Course_Materials
                    (course_id, title, m_id, content_url, content_text, order_index)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    course_id,
                    material.get("title"),
                    material.get("m_id"),
                    material.get("content_url"),
                    material.get("content_text"),
                    material.get("order_index", 0)
                ))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()