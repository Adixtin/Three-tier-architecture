from datetime import datetime

class Controller:
    ALLOWED_GROUPS = {"admin", "user", "guest"}

    def __init__(self, repository):
        self.repository = repository

    def create(self, data):
        if not self.validate_data(data):
            return {"error": "Invalid user data"}, 400
        user = self.repository.add(data)
        if user:
            return user, 201
        return {"error": "Failed to create user"}, 500

    def get(self):
        return self.repository.get(), 200

    def get_by_id(self, user_id):
        if not isinstance(user_id, int) or user_id < 0:
            return {"error": "Invalid user Id"}, 400
        user = self.repository.get_by_id(user_id)
        if user:
            return user, 200
        return {"error": "User not found"}, 400

    def update(self, user_id, update_data):
        if not isinstance(user_id, int) or user_id < 0:
            return {"error": "Invalid user Id"}, 400

        if not self.validate_update_data(update_data):
            return {"error": "Invalid update data"}, 400

        user = self.repository.update(user_id, update_data)
        if user:
            return user, 200
        return {"error": "User not found"}, 404

    def delete(self, user_id):
        if not isinstance(user_id, int) or user_id < 0:
            return {"error": "Invalid user ID"}, 400

        user = self.repository.delete(user_id)
        if user:
            return user, 200
        return {"error": "User not found"}, 404

    def validate_data(self, data):
        required_fields = {"firstName", "lastName", "birthYear", "group"}
        if not all(field in data for field in required_fields):
            return False

        if not isinstance(data["firstName"], str) or not isinstance(data["lastName"], str):
            return False
        if not isinstance(data["birthYear"], int) or data["birthYear"] <= 1900 or data["birthYear"] > datetime.now().year:
            return False
        if data["group"] not in self.ALLOWED_GROUPS:
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