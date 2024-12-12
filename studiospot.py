from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for production
bcrypt = Bcrypt(app)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': '',  
    'database': 'StudioSpotDB'
}

# Function to create database if it doesn't exist
def create_database():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS StudioSpotDB")
        print("Database 'StudioSpotDB' created or already exists.")
    finally:
        cursor.close()
        conn.close()

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.before_first_request
def setup_database():
    create_database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fetch user from database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert new user into database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            flash('Error: ' + str(e), 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return "Welcome to your dashboard!"
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_database()  # Ensure the database exists before running the app
    app.run(debug=True)
