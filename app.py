from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "sqli_demo_secret"

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    c.execute("DELETE FROM users")
    c.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
        ("admin", "admin@123", "Administrator"),
        ("gargi", "pass123", "Student"),
        ("teacher", "teach@456", "Teacher"),
    ])
    conn.commit()
    conn.close()

def vulnerable_login(username, password):
    """VULNERABLE: directly concatenates user input into SQL query."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        c.execute(query)
        results = c.fetchall()
        user = results[0] if results else None
    except Exception as e:
        conn.close()
        return None, query, str(e)
    conn.close()
    return user, query, None

def secure_login(username, password):
    """SECURE: uses parameterised queries — SQL injection is impossible."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    c.execute(query, (username, password))
    user = c.fetchone()
    conn.close()
    return user, query

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    mode = request.args.get("mode", "vulnerable")
    result = None
    query_shown = None
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        mode = request.form.get("mode", "vulnerable")

        if mode == "vulnerable":
            user, query_shown, error = vulnerable_login(username, password)
        else:
            user, query_shown = secure_login(username, password)
            error = None

        if user and not error:
            session["user"] = user[1]
            session["role"] = user[3]
            session["mode"] = mode
            session["query"] = query_shown
            return redirect(url_for("dashboard"))

        result = "failed"

    return render_template("login.html",
                           mode=mode,
                           result=result,
                           query_shown=query_shown,
                           error=error)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html",
                           user=session["user"],
                           role=session["role"],
                           mode=session.get("mode"),
                           query=session.get("query"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
