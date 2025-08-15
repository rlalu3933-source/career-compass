from flask import Flask, render_template, request, redirect, flash, url_for # pyright: ignore[reportMissingImports]
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user # type: ignore
from utils.quiz_logic import evaluate_quiz
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 🔐 Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 👤 User class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# 🔄 Load user from DB
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(*user)
    return None

# 🏠 Home page
@app.route('/')
def home():
    return render_template('index.html')

# 📝 Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
        conn.close()
    return render_template('signup.html')

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            login_user(User(*user))
            flash("Logged in successfully!", "success")
            return redirect(url_for('quiz'))
        else:
            flash("Invalid credentials.", "danger")
    return render_template('login.html')

# 🚪 Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('login'))

# 🎯 Career Quiz (protected)
@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

# 📊 Quiz Results (protected)
@app.route('/results', methods=['POST'])
@login_required
def results():
    answers = request.form
    career = evaluate_quiz(answers)
    return render_template('results.html', career=career)

# 🧭 Run the app
if __name__ == '__main__':
    app.run(debug=True)
