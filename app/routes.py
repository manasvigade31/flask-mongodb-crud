from flask import Blueprint, jsonify, request
from email_validator import validate_email, EmailNotValidError
from app.models import User
from app.schemas import UserSchema
from app import mongo
import bcrypt
import re

app = Blueprint('app', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.route('/health', methods=['GET'])
def health_check():
    try:
        mongo.db.command("ping")  
        return jsonify({"status": "MongoDB is connected"}), 200
    except Exception as e:
        return jsonify({"status": "MongoDB connection failed", "error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()  
    result = users_schema.dump(users)  
    return jsonify(result)  

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({"_id": id}) 
    if user:
        result = user_schema.dump(user)  
        return jsonify(result)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        valid_email = validate_email(data['email']) 
        email = valid_email.email
    except EmailNotValidError as e:
        return jsonify({"error": f"Invalid email: {str(e)}"}), 400
    
    password = data['password']
    if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        return jsonify({"error": "Password must be at least 8 characters long, include letters and numbers."}), 400
    
    hashed_password = hash_password(password)
    
    new_user = {
        'name': data['name'],
        'email': data['email'],
        'password': hashed_password
    }
    mongo.db.users.insert_one(new_user)  
    return jsonify({"message": "User created successfully"}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = mongo.db.users.find_one({"email": data['email']})
#     if user and User.verify_password(user['password'], data['password']):
#         return jsonify({"message": "Login successful"}), 200
#     return jsonify({"message": "Invalid email or password"}), 401

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    updated_user = mongo.db.users.find_one_and_update(
        {"_id": id}, {"$set": data}, return_document=True
    )
    if updated_user:
        result = user_schema.dump(updated_user) 
        return jsonify(result)
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = mongo.db.users.delete_one({"_id": id})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"}), 204
    return jsonify({"error": "User not found"}), 404
