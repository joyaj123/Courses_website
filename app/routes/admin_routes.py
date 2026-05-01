from flask import jsonify
from app.models.admin import get_dashboard_stats
from app.utils.jwt_handler import get_user_id_from_token

def dashboard_stats():
    user_id=get_user_id_from_token()

    if not user_id:
        return jsonify({"error": "UNauthorized"}),401
    
    stats=get_dashboard_stats

    return jsonify ({
        "message":"Dashboard stats fetched successfully",
        "data":stats
    
    }),200