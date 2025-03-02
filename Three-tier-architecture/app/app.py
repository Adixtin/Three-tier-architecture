from flask import Flask, jsonify, request
from app.repositry import Repository
from app.controller import Controller
app = Flask(__name__)


repository = Repository()
service = Controller(repository)

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
