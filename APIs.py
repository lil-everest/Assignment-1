from flask import Flask, request, jsonify
from passlib.hash import argon2
import uuid
import sqlite3

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = str(uuid.uuid4())

    hashed_password = argon2.hash(password)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
        (username, email, hashed_password)
    )
    conn.commit()
    conn.close()

    return jsonify({"password": password}), 201
