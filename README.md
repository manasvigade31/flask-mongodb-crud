# Flask MongoDB CRUD Application

This is a Flask application that provides RESTful API endpoints for performing CRUD (Create, Read, Update, Delete) operations on a MongoDB database. The application includes features such as password hashing, email validation, and Dockerization for ease of deployment.

---

## **Features**

- User resource management with CRUD operations.
- Password hashing using `bcrypt` for enhanced security.
- Email validation to ensure valid email addresses.
- Dockerized setup for consistent deployment.
- Modular and scalable code structure.

---

## **Getting Started**

### **Prerequisites**

Ensure you have the following installed:

- Python 3.8+
- Docker and Docker Compose
- MongoDB

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
    pip install -r requirements.txt

4. Running the Application

    Build the Docker containers:

    docker-compose build

    Start the application:

    docker-compose up

    Access the API at http://127.0.0.1:5000/users

5. API Endpoints

    User Endpoints
    
    1. Create a User
    Endpoint: POST /users
    Description: Creates a new user with a hashed password.
    Request Body:
    {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123"
    }

    Response:
    {
    "message": "User created successfully"
    }

    2. Get All Users
    Endpoint: GET /users
    Description: Retrieves a list of all users.
    3. Update a User
    Endpoint: PUT /users/<user_id>
    Description: Updates user details.
    4. Delete a User
    Endpoint: DELETE /users/<user_id>
    Description: Deletes a user.


6. Environment Variables:

    Create a .env file in the project root with the following:

    FLASK_ENV=development
    MONGO_URI=mongodb://mongodb:27017/flask_app_db
    SECRET_KEY=your-secret-key


Security Features
    Password Hashing: Passwords are stored as hashed values using bcrypt, ensuring they are not stored in plaintext.
    Email Validation: Ensures that all email addresses follow a valid format using the email-validator library.
    Environment Variables: Secrets like database URIs and secret keys are managed using .env.