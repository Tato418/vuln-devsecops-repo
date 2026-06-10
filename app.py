
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- Vulnerabilities ---

# 1. Security Misconfiguration: Debug mode enabled
# This should NEVER be enabled in a production environment.
app.config['DEBUG'] = True

# 2. Sensitive Data Exposure: Hardcoded API key
# In a real application, this should be stored securely (e.g., environment variables, secrets manager)
DUMMY_API_KEY = "super_secret_insecure_api_key_12345"

# Mock in-memory database for demonstration
users_db = [
    {"id": 1, "username": "alice", "password": "password123"},
    {"id": 2, "username": "bob", "password": "securepassword456"},
]

# --- Routes ---

@app.route('/')
def home():
    return "Welcome to the Vulnerable DevSecOps App!"

@app.route('/users', methods=['GET'])
def get_users():
    # Basic endpoint to list users
    # In a real scenario, this might fetch from a DB.
    # For simplicity, we return the list, but sensitive info like passwords are not intended to be here.
    # The password is here for demonstration purposes to show it's not being handled securely.
    return jsonify(users_db)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # 3. Insecure Direct Object Reference (IDOR) - Potential if not properly authorized
    # If the system had authentication and authorization, it would check if the current user
    # is allowed to view the requested user_id. Here, anyone can request any user_id.

    # 4. SQL Injection (Simulated):
    # If this were a real SQL database, a query like f"SELECT * FROM users WHERE id = {user_id}"
    # would be vulnerable to SQL injection.
    # Here, we're filtering a list, but the GET parameter `user_id` is directly used.
    # A more realistic simulation might involve a direct string concatenation with a SQL query.
    
    # For demonstration, let's simulate a vulnerable query string construction
    # In a real app, you'd use parameterized queries: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    # Simulated vulnerable query construction:
    # query = f"SELECT * FROM users WHERE id = {user_id}" # This is the vulnerable part if it was SQL

    user = next((user for user in users_db if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    # 5. Broken Authentication / Weak Passwords:
    # Storing and comparing plain text passwords or weak hashes.
    # This example uses plain text passwords for simplicity and demonstration.
    
    user = next((user for user in users_db if user['username'] == username), None)
    
    if user and user['password'] == password:
        # 6. Cross-Site Scripting (XSS) - Reflected XSS:
        # If username was displayed directly in HTML response without escaping.
        # Example: <p>Welcome, {username}!</p>
        # Here, we are returning JSON, so direct XSS in JSON is less common, but if rendered
        # in a web page dynamically, the username might be echoed without escaping.
        # Let's simulate it by crafting a simple HTML response if a GET request was used.
        # For POST JSON response, we'll just return success.
        
        # Simulating potential XSS if response was HTML and username was directly embedded
        return jsonify({"message": f"Login successful, welcome {username}!"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/data', methods=['GET'])
def get_api_data():
    # Example of using the hardcoded API key
    api_key_header = request.headers.get('X-API-Key')
    if api_key_header == DUMMY_API_KEY:
        return jsonify({"data": "Sensitive information fetched successfully", "api_key_used": DUMMY_API_KEY})
    else:
        return jsonify({"message": "Unauthorized"}), 401

if __name__ == '__main__':
    # Host on 0.0.0.0 to be accessible externally (useful for Docker/Kubernetes)
    app.run(host='0.0.0.0', port=5000)
