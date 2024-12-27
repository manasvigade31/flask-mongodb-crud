from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB (make sure MongoDB is running)
client = MongoClient("mongodb://localhost:27017/")
db = client["flask_mongo"]
users_collection = db["users"]


@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        users_count = users_collection.count_documents({})
        return jsonify({"message": "MongoDB connected", "user_count": users_count}), 200
    except Exception as e:
        return jsonify({"message": "Failed to connect to MongoDB", "error": str(e)}), 500


# Create user (POST)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        "name": data['name'],
        "email": data['email'],
        "password": data['password']
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User created"}), 201

# Get all users (GET)
@app.route('/users', methods=['GET'])
def get_users():
    users = users_collection.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        user_list.append(user)
    return jsonify(user_list)

# Get a user by ID (GET)
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = users_collection.find_one({"_id": ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

# Update user (PUT)
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    result = users_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.matched_count > 0:
        return jsonify({"message": "User updated"})
    return jsonify({"message": "User not found"}), 404

# Delete user (DELETE)
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = users_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted"})
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
