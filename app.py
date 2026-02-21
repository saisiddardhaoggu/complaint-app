from flask import Flask, render_template, request, send_file
from complaint_generator import generate_complaint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database import get_db_connection, init_db
from datetime import datetime
from flask import session, redirect, url_for
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from flask import send_file

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

    if request.method == "POST":

        name = request.form.get("name")
        phone = request.form.get("phone")
        branch = request.form.get("location")   # 🔥 change here
        college = request.form.get("station")  # 🔥 change here
        description = request.form.get("description")

        date = "N/A"  # Since no date field in form

        if not all([name, phone, branch, college, description]):
            return "Form data missing"

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO complaints 
            (name, phone, branch, college, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, phone, branch, college, description, date))

        conn.commit()
        conn.close()

        return render_template(
    "letter.html",
    name=name,
    phone=phone,
    branch=branch,
    college=college,
    description=description,
    date=date
)

    return render_template("index.html")

@app.route("/download")
def download_file():
    return send_file("complaint.pdf", as_attachment=True)

import sqlite3

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["admin"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    complaints = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", complaints=complaints)

import re
@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        new_password = request.form["password"]

        if len(new_password) < 8:
            return "Password must be at least 8 characters"

        conn = get_db_connection()
        conn.execute(
            "UPDATE admin SET password=? WHERE username=?",
            (new_password, session["admin"])
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("change_password.html")
@app.route("/download_letter")
def download_letter():

    conn = get_db_connection()
    complaint = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if not complaint:
        return "No complaint found"

    file_path = "complaint_letter.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    text = f"""
    To,
    The Principal,
    {complaint['college']}

    Subject: Complaint regarding issue in {complaint['branch']} department

    I, {complaint['name']}, would like to bring to your notice:

    {complaint['description']}

    Kindly take necessary action.

    Yours sincerely,
    {complaint['name']}
    Phone: {complaint['phone']}
    Date: {complaint['date']}
    """

    elements.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))
    doc.build(elements)

    return send_file(file_path, as_attachment=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
