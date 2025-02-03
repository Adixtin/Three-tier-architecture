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

if __name__ == "__main__":
    app.run(debug=True)