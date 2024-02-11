from flask import Flask, request, jsonify, session
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS
from itsdangerous import URLSafeSerializer



app = Flask(__name__)
CORS(app) # Add this line to enable CORS for all routes
app.secret_key = 'jgwvhdhawdfhjwefjhwefjh'  # Set a secret key for session management



# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



# Function to send email
def send_email(receiver_email, message):
    sender_email = 'company_email@example.com'  # company email address
    password = 'email_password'  # company email password
    
    msg = MIMEText(message)
    msg['Subject'] = 'Password Reset'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False




# Route for handling user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = hash_password(data['password'])

    # Store registration data in SQLite database
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# Route for handling user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = hash_password(data['password'])

    # Validate login credentials against SQLite database
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and user[3] == password:
            session['logged_in'] = True
            session['user_id'] = user[2]  # Save user ID in session
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# Route for handling password reset
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data['email']

    # Check if email exists in the database
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Generate and send reset password email
            reset_link = 'http://your_website.com/reset-password'  # Example reset link
            message = f"Click the following link to reset your password: {reset_link}"
            if send_email(email, message):
                return jsonify({'message': 'Password reset email sent'})
            else:
                return jsonify({'message': 'Failed to send password reset email'}), 500
        else:
            return jsonify({'message': 'Email not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500




# Route for handling user logout
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear session data
    return jsonify({'message': 'Logout successful'})


if __name__ == '__main__':
    app.run(debug=True)
