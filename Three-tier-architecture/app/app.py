from flask import Flask, jsonify, request
from app.repository import Repository  # Fixed typo
from app.controller import Controller

app = Flask(__name__)

# Initialize repository and controller
repository = Repository()
service = Controller(repository)

@app.route("/users", methods=["GET"])
def get_users():
    users, status = service.get()
    return jsonify(users), status

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user, status = service.get_by_id(user_id)
    return jsonify(user), status

@app.route("/users", methods=["POST"])
def add_user():
    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No user data provided"}), 400

    user, status = service.create(user_data)  # Fixed method name
    return jsonify(user), status

@app.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No update data provided"}), 400

    user, status = service.update(user_id, update_data)
    return jsonify(user), status

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user, status = service.delete(user_id)  # Fixed method name
    return jsonify(user), status

if __name__ == "__main__":
    app.run(debug=True)