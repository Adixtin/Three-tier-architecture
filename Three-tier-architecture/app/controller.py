
from app.repositry import Repository 

class Controller:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, user_data):
        if not self.validate_user_data(user_data):
            return None, 400
        return self.repository.add_user(user_data), 201

    def get_all_users(self):
        return self.repository.get_users(), 200

    def get_user_by_id(self, user_id):
        if not isinstance(user_id, int) or user_id < 0:
            return {"error": "Invalid user Id"}, 400
        user = self.repository.get_user_by_id(user_id)
        if user:
            return user, 200
        return {"error": "User not found"}, 400

    def update_user(self, user_id, update_data):
        if not isinstance(user_id, int) or user_id < 0:
            return {"error": "Invalid user Id"}, 400

        # Validate the update data
        if not self.validate_update_data(update_data):
            return {"error": "Invalid update data"}, 400

        user = self.repository.update_user(user_id, update_data)
        if user:
            return user, 200
        return {"error": "User not found"}, 404

    def delete_user(self, user_id):
        if not isinstance(user_id, int) or user_id < 0:
            return {"error": "Invalid user ID"}, 400

        user = self.repository.delete_user(user_id)

        if user:
            return user, 200
        return {"error": "User not found"}, 404

    def validate_user_data(self, user_data):
        required_fields = {"firstName", "lastName", "birthYear", "group"}
        if not all(field in user_data for field in required_fields):
            return False

        if not isinstance(user_data["firstName"], str) or not isinstance(user_data["lastName"], str):
            return False
        if not isinstance(user_data["birthYear"], int) or user_data["birthYear"] <= 1900 or user_data["birthYear"] > datetime.now().year:
            return False
        if user_data["group"] not in self.ALLOWED_GROUPS:
            return False
        return True

    def validate_update_data(self, update_data):
        allowed_fields = {"firstName", "lastName", "birthYear", "group"}
        if not any(field in update_data for field in allowed_fields):
            return False
        if "firstName" in update_data and not isinstance(update_data["firstName"], str):
            return False
        if "lastName" in update_data and not isinstance(update_data["lastName"], str):
            return False
        if "birthYear" in update_data and (not isinstance(update_data["birthYear"], int) or update_data["birthYear"] <= 1900 or update_data["birthYear"] > datetime.now().year):
            return False
        if "group" in update_data and update_data["group"] not in self.ALLOWED_GROUPS:
            return False
        return True

