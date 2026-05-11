from flask import render_template
from app.models.learning import get_learning_page_data


def learning_page(course_id, lesson_id):
    data = get_learning_page_data(course_id, lesson_id)

    if not data:
        return render_template("lesson_player.html", data=None, error="Lesson not found")

    return render_template("lesson_player.html", data=data)