from app import mongo
from app import bcrypt

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')  

    def save(self):
       
        mongo.db.users.insert_one({
            "name": self.name,
            "email": self.email,
            "password": self.password
        })

    @staticmethod
    def verify_password(hashed_password, plain_password):
        return bcrypt.check_password_hash(hashed_password, plain_password)
    
    @staticmethod
    def get_all():
        try:
            users = mongo.db.users.find() 
            return list(users) 
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        user_data = mongo.db.users.find_one({"_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    def save(self):
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password 
        }
        result = mongo.db.users.insert_one(user_data)
        self.id = result.inserted_id
        return self

    @staticmethod
    def update(user_id, data):
        mongo.db.users.update_one({"_id": user_id}, {"$set": data})
        return User.get_by_id(user_id)

    @staticmethod
    def delete(user_id):
        mongo.db.users.delete_one({"_id": user_id})

