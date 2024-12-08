@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    request_ip = request.remote_addr

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check user
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and argon2.verify(password, user[1]):
        # Log authentication request
        cursor.execute(
            "INSERT INTO auth_logs (request_ip, user_id) VALUES (?, ?)", 
            (request_ip, user[0])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Authenticated"}), 200
    else:
        conn.close()
        return jsonify({"message": "Unauthorized"}), 401
