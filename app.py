from flask import Flask, render_template, request, send_file
from complaint_generator import generate_complaint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database import init_db, insert_complaint
from database import get_complaints
from datetime import datetime
from flask import session, redirect, url_for
from database import update_password
import os


app = Flask(__name__)
app.secret_key = "college_secret_key"
init_db()

def create_pdf(text):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    file_path = "complaint.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    x = 40
    y = 750
    max_chars = 80  # line width control

    for line in text.split("\n"):
        while len(line) > max_chars:
            c.drawString(x, y, line[:max_chars])
            line = line[max_chars:]
            y -= 15
        c.drawString(x, y, line)
        y -= 15

    c.save()
    return file_path

@app.route("/", methods=["GET", "POST"])
def home():
    complaint = ""

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        branch = request.form.get("location")
        college = request.form.get("station")
        description = request.form.get("description")

        from datetime import datetime
        date = datetime.now().strftime("%d-%m-%Y")

        complaint = generate_complaint(
            name, phone, date, branch, college, description
        )

        insert_complaint(name, phone, date, branch, college, description)
        create_pdf(complaint)

    return render_template("index.html", complaint=complaint)




@app.route("/download")
def download_file():
    return send_file("complaint.pdf", as_attachment=True)

import sqlite3

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("complaints.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    complaints = get_complaints()
    return render_template("dashboard.html", complaints=complaints)

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        new_password = request.form.get("password")
        update_password(session["user"], new_password)
        return redirect("/dashboard")

    return render_template("change_password.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)