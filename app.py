import os
from flask import Flask, render_template_string, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "kes_carmel_secret_key"

# Connect to MongoDB using Vercel's automatic environment variable
MONGO_URI = os.environ.get("STORAGE_URL")
client = MongoClient(MONGO_URI)
db = client["school_portal_db"]
students_collection = db["students"]

# Single HTML Template with Neon Cyberpunk Design
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K.E. Carmel School, Bankura - Student Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #05050a;
            --panel-bg: rgba(15, 15, 30, 0.7);
            --neon-cyan: #00f3ff;
            --neon-pink: #ff007f;
            --neon-green: #00ff66;
            --text-main: #e0e0ff;
            --border-glow: 0 0 15px rgba(0, 243, 255, 0.4);
            --pink-glow: 0 0 15px rgba(255, 0, 127, 0.4);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; overflow-x: hidden; background-image: radial-gradient(circle at 50% 10%, #111025 0%, #05050a 90%); }

        header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 20px 50px; border-bottom: 1px solid rgba(0, 243, 255, 0.2);
            background: rgba(5, 5, 10, 0.8); backdrop-filter: blur(10px);
            position: sticky; top: 0; z-index: 1000;
        }

        .logo { font-family: 'Orbitron', sans-serif; font-weight: 800; font-size: 1.5rem; color: var(--neon-cyan); text-shadow: var(--border-glow); }
        nav a { color: var(--text-main); text-decoration: none; margin-left: 20px; font-weight: 600; transition: 0.3s; }
        nav a:hover { color: var(--neon-cyan); text-shadow: var(--border-glow); }

        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }

        /* Hero Section */
        .hero {
            text-align: center; padding: 60px 20px; background: var(--panel-bg);
            border: 1px solid rgba(0, 243, 255, 0.3); border-radius: 15px;
            box-shadow: var(--border-glow); margin-bottom: 40px; position: relative; overflow: hidden;
        }
        .hero h1 { font-family: 'Orbitron', sans-serif; font-size: 2.8rem; color: var(--neon-cyan); text-shadow: var(--border-glow); margin-bottom: 15px; }
        .hero p { font-size: 1.1rem; color: #a5b4fc; max-width: 800px; margin: 0 auto 25px auto; line-height: 1.6; }

        .btn-neon {
            background: transparent; color: var(--neon-cyan); border: 2px solid var(--neon-cyan);
            padding: 12px 30px; font-family: 'Orbitron', sans-serif; font-weight: 600;
            border-radius: 8px; cursor: pointer; text-shadow: var(--border-glow);
            box-shadow: var(--border-glow); transition: 0.3s; text-decoration: none; display: inline-block;
        }
        .btn-neon:hover { background: var(--neon-cyan); color: #000; box-shadow: 0 0 30px var(--neon-cyan); }

        .btn-pink {
            color: var(--neon-pink); border-color: var(--neon-pink); text-shadow: var(--pink-glow); box-shadow: var(--pink-glow);
        }
        .btn-pink:hover { background: var(--neon-pink); color: #fff; box-shadow: 0 0 30px var(--neon-pink); }

        /* Panels / Cards */
        .panel {
            background: var(--panel-bg); border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            backdrop-filter: blur(8px);
        }
        .panel h2 { font-family: 'Orbitron', sans-serif; color: var(--neon-cyan); margin-bottom: 20px; font-size: 1.5rem; text-shadow: var(--border-glow); }

        /* Form Controls */
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .form-group { display: flex; flex-direction: column; }
        label { font-size: 0.9rem; color: #a5b4fc; margin-bottom: 8px; font-weight: 600; }
        input, select, textarea {
            background: rgba(10, 10, 20, 0.9); border: 1px solid rgba(0, 243, 255, 0.4);
            padding: 12px; border-radius: 6px; color: #fff; font-size: 1rem; outline: none; transition: 0.3s;
        }
        input:focus, select:focus, textarea:focus { border-color: var(--neon-cyan); box-shadow: var(--border-glow); }

        /* Tables & Lists */
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 14px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }
        th { font-family: 'Orbitron', sans-serif; color: var(--neon-cyan); font-size: 0.9rem; }
        tr:hover { background: rgba(0, 243, 255, 0.05); }

        .actions a { margin-right: 15px; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
        .edit-btn { color: var(--neon-green); }
        .del-btn { color: var(--neon-pink); }

        .class-section-header { font-family: 'Orbitron', sans-serif; color: var(--neon-pink); margin: 25px 0 10px 0; font-size: 1.2rem; text-shadow: var(--pink-glow); border-bottom: 1px dashed var(--neon-pink); padding-bottom: 5px; }

        .alert-error { background: rgba(255, 0, 127, 0.2); border: 1px solid var(--neon-pink); padding: 12px; border-radius: 6px; color: #ff80bf; margin-bottom: 20px; text-align: center; }
    </style>
</head>
<body>

    <header>
        <div class="logo">⚡ K.E. CARMEL BANKURA</div>
        <nav>
            <a href="/">Home</a>
            {% if session.get('admin') %}
                <a href="/dashboard">Dashboard</a>
                <a href="/logout">Logout</a>
            {% else %}
                <a href="/login">Admin Portal</a>
            {% endif %}
        </nav>
    </header>

    <div class="container">
        {% if view == 'home' %}
            <div class="hero">
                <h1>K.E. Carmel School, Bankura</h1>
                <p>Welcome to the next-generation digital portal of K.E. Carmel School, Bankura. Fostering academic excellence, discipline, and advanced technological values in a premier futuristic learning environment.</p>
                <a href="/dashboard" class="btn-neon">Access Admin Dashboard</a>
            </div>
        {% elif view == 'login' %}
            <div class="panel" style="max-width: 450px; margin: 0 auto;">
                <h2>🔐 Admin Authentication</h2>
                {% if error %}
                    <div class="alert-error">{{ error }}</div>
                {% endif %}
                <form method="POST" action="/login">
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label>Username</label>
                        <input type="text" name="username" placeholder="Enter admin..." required>
                    </div>
                    <div class="form-group" style="margin-bottom: 25px;">
                        <label>Password</label>
                        <input type="password" name="password" placeholder="Enter 12345..." required>
                    </div>
                    <button type="submit" class="btn-neon" style="width: 100%;">Login System</button>
                </form>
            </div>
        {% elif view == 'dashboard' %}
            <div class="panel">
                <h2>⚡ Add New Student Record</h2>
                <form method="POST" action="/add">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" name="name" placeholder="e.g. Arnesh" required>
                        </div>
                        <div class="form-group">
                            <label>Class</label>
                            <select name="class_name" required>
                                <option value="">Select Class</option>
                                {% for c in range(1, 13) %}
                                    <option value="Class {{ c }}">Class {{ c }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Section</label>
                            <select name="section" required>
                                <option value="A">Section A</option>
                                <option value="B">Section B</option>
                                <option value="C">Section C</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Class Roll Number</label>
                            <input type="number" name="roll" placeholder="e.g. 15" required>
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 20px;">
                        <label>Personal Details / Bio / Notes</label>
                        <textarea name="details" rows="3" placeholder="Interests, contact info, remarks..."></textarea>
                    </div>
                    <button type="submit" class="btn-neon btn-pink">Upload to Database (.txt)</button>
                </form>
            </div>

            <div class="panel">
                <h2>📂 Organized Student Directory</h2>
                {% if not students %}
                    <p style="color: #a5b4fc;">No student records found in local storage.</p>
                {% else %}
                    {% set grouped = {} %}
                    {% for s in students %}
                        {% if s.class_name not in grouped %}{% set _ = grouped.update({s.class_name: []}) %}{% endif %}
                        {% set _ = grouped[s.class_name].append(s) %}
                    {% endfor %}

                    {% for class_name, class_students in grouped.items() %}
                        <div class="class-section-header">🏫 {{ class_name }}</div>
                        <table>
                            <thead>
                                <tr>
                                    <th>Roll</th>
                                    <th>Name</th>
                                    <th>Sec</th>
                                    <th>Personal Details</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for s in class_students %}
                                <tr>
                                    <td><strong>#{{ s.roll }}</strong></td>
                                    <td>{{ s.name }}</td>
                                    <td>{{ s.section }}</td>
                                    <td style="color: #a5b4fc; font-size: 0.9rem;">{{ s.details }}</td>
                                    <td class="actions">
                                        <a href="/edit/{{ s.id }}" class="edit-btn">Edit</a>
                                        <a href="/delete/{{ s.id }}" class="del-btn" onclick="return confirm('Are you sure you want to delete this record?');">Delete</a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    {% endfor %}
                {% endif %}
            </div>
        {% elif view == 'edit' %}
            <div class="panel" style="max-width: 600px; margin: 0 auto;">
                <h2>✏️ Edit Student Record</h2>
                <form method="POST" action="/update/{{ student.id }}">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" name="name" value="{{ student.name }}" required>
                        </div>
                        <div class="form-group">
                            <label>Class</label>
                            <select name="class_name" required>
                                {% for c in range(1, 13) %}
                                    <option value="Class {{ c }}" {% if student.class_name == 'Class ' ~ c %}selected{% endif %}>Class {{ c }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Section</label>
                            <select name="section" required>
                                <option value="A" {% if student.section == 'A' %}selected{% endif %}>Section A</option>
                                <option value="B" {% if student.section == 'B' %}selected{% endif %}>Section B</option>
                                <option value="C" {% if student.section == 'C' %}selected{% endif %}>Section C</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Roll Number</label>
                            <input type="number" name="roll" value="{{ student.roll }}" required>
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 20px;">
                        <label>Personal Details</label>
                        <textarea name="details" rows="3">{{ student.details }}</textarea>
                    </div>
                    <button type="submit" class="btn-neon">Save Changes</button>
                    <a href="/dashboard" style="margin-left: 15px; color: #a5b4fc; text-decoration: none;">Cancel</a>
                </form>
            </div>
        {% endif %}
    </div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(TEMPLATE, view="home")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "12345":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            error = "Invalid Credentials! Use username: admin and password: 12345"
    return render_template_string(TEMPLATE, view="login", error=error)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"): return redirect("/login")
    students = list(students_collection.find())
    for s in students: s["id"] = str(s["_id"])
    return render_template_string(TEMPLATE, view="dashboard", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    if not session.get("admin"): return redirect("/login")
    new_record = {
        "name": request.form.get("name"),
        "class_name": request.form.get("class_name"),
        "section": request.form.get("section"),
        "roll": request.form.get("roll"),
        "details": request.form.get("details", "")
    }
    students_collection.insert_one(new_record)
    return redirect("/dashboard")

@app.route("/edit/<student_id>")
def edit_student(student_id):
    if not session.get("admin"): return redirect("/login")
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student: student["id"] = str(student["_id"])
    return render_template_string(TEMPLATE, view="edit", student=student)

@app.route("/update/<student_id>", methods=["POST"])
def update_student(student_id):
    if not session.get("admin"): return redirect("/login")
    students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {
            "name": request.form.get("name"),
            "class_name": request.form.get("class_name"),
            "section": request.form.get("section"),
            "roll": request.form.get("roll"),
            "details": request.form.get("details", "")
        }}
    )
    return redirect("/dashboard")

@app.route("/delete/<student_id>")
def delete_student(student_id):
    if not session.get("admin"): return redirect("/login")
    students_collection.delete_one({"_id": ObjectId(student_id)})
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
