from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

class UserRepository:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def add_user(self, user_data):
        user = {
            "id": self.next_id,
            "firstName": user_data["firstName"],
            "lastName": user_data["lastName"],
            "age": datetime.now().year - user_data["birthYear"],
            "group": user_data["group"]
        }
        self.users.append(user)
        self.next_id += 1
        return user

    def get_users(self):
        return self.users

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None

    def update_user(self, user_id, update_data):
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in update_data.items():
                # Always update age if 'birthYear' is provided,
                # even if 'birthYear' is not in the user dict.
                if key == "birthYear":
                    user["age"] = datetime.now().year - value
                    # Optionally, also store the birthYear if you need it later.
                    user[key] = value
                elif key in user:
                    user[key] = value
            return user
        return None

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.users = [u for u in self.users if u["id"] != user_id]
            return user
        return None

class UserService:
    ALLOWED_GROUPS = {"user", "premium", "admin"}

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

repository = UserRepository()
service = UserService(repository)

@app.route("/users", methods=["GET"])
def get_users():
    users, status = service.get_all_users()
    return jsonify(users), status

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user, status = service.get_user_by_id(user_id)
    return jsonify(user), status

@app.route("/users", methods=["POST"])
def add_user():
    user_data = request.get_json()
    user, status = service.create_user(user_data)
    if user is None:
        return jsonify({"error": "Invalid user data"}), status
    return jsonify(user), status

@app.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No update data provided"}), 400

    user, status = service.update_user(user_id, update_data)
    return jsonify(user), status

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user, status = service.delete_user(user_id)
    return jsonify(user), status


if __name__ == "__main__":
    app.run(debug=True)