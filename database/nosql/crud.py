from pymongo import MongoClient
from utils import log_error, generate_random_id

class CRUD:
    def __init__(self, db_name: str, collection_name: str):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, data: dict) -> bool:
        try:
            data["_id"] = generate_random_id()
            self.collection.insert_one(data)
            return True
        except Exception as err:
            log_error(str(err))
            return False
    
    def read(self, data: tuple[str, object]) -> dict:
        try:
            result = self.collection.find_one({
                data[0]: data[1]
            })
            return {} if not result else result
        except Exception as err:
            log_error(str(err))
            return {}
    
    def update(self, data: tuple[str, object]) -> bool:
        try:
            result = self.collection.update_one({
                data[0]: {"$set":data[1]}
            })
            return True if (result.matched_count == 1 and result.modified_count == 1) else False
        except Exception as err:
            log_error(str(err))
            return False
    
    def replace(self, data: tuple[str, object]) -> bool:
        try:
            result = self.collection.replace_one(
                {
                    "_id": data["_id"]
                },
                data,
                True
            )
            return True if (result.matched_count == 1 and result.modified_count == 1) else False
        except Exception as err:
            log_error(str(err))
            return False
    
    def delete(self, data: tuple[str, object]) -> bool:
        try:
            result = self.collection.delete_one({
                data[0]: data[1]
            })
            return True if (result.matched_count == 1 and result.modified_count == 1) else False
        except Exception as err:
            log_error(str(err))
            return False
    
    
    

