from app.models.user import get_user_by_id

def is_admin(user_id):
    user=get_user_by_id(user_id)

    if not user:
        return False
    
    return user["role"]=="admin"