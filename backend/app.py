from flask import Flask, render_template, request, redirect, session, url_for
from db import init_db, save_user, validate_user, save_run_to_db, get_user_runs
from model_utils import (
    predict_t1_from_total,
    predict_t2_from_total,
    predict_t3,
    analyze_performance,
    categorize_athlete,
    analyze_run
)
import os

app = Flask(__name__)
app.secret_key = "sprint_secret_key"

init_db()

@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if save_user(username, password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Username already exists!"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if validate_user(username, password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials!"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    runs = get_user_runs(username)
    return render_template("dashboard.html", runs=runs)

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        total_time = float(request.form["total_time"])
        t1 = request.form.get("t1")
        t2 = request.form.get("t2")

        t1 = float(t1) if t1 else None
        t2 = float(t2) if t2 else None

        result = analyze_run(total_time, t1, t2)

        save_run_to_db(session["username"], result)

        return render_template("result.html", result=result)

    return render_template("analyze.html")

if __name__ == "__main__":
    app.run(debug=True)
