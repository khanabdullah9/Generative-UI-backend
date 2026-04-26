from pymongo import MongoClient

from utils import log_error, generate_random_id

client = MongoClient()
db = client["FastApp"]

def create_collection(coll_name: str, user_name: str, user_id: int) -> bool:
    try:
        
        db["_".join([coll_name, user_name, str(user_id)])]
    except Exception as err:
        log_error(str(err))
        return False
    
def add_user(user_name: str, email: str) -> bool:
    try:
        result = db.project_users.insert_one({
            "_id": generate_random_id(),
            "user": user_name,
            "email": email,
            "password": "test@1234" # initial password
        })
        return True if result.inserted_id else False
    except Exception as err:
        log_error(str(err))
        return False
    
def replace_user(id: str, user_name: str, email,password: str) -> bool:
    try:
        result = db.project_users.replace_one(
        {
            "_id": id
        },
        {
            "_id": id,
            "user": user_name,
            "email": email,
            "password": password
        },
        True)
        return True if (result.matched_count > 0 and result.modified_count > 0) else False
    except Exception as err:
        log_error(str(err))
        return False
    
def update_user_password(id: str, new_password: str) -> bool:
    try:
        result = db.project_users.update_one(
            {
                "_id":id
            },
            {
                "$set": {
                    "password": new_password
                }
            }
        )
        return True if (result.matched_count > 0 and result.modified_count > 0) else False
    except Exception as err:
        log_error(str(err))
        return False
