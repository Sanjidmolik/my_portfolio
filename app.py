from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for sessions

# Home page routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_message = {"name": name, "email": email, "message": message}

        try:
            with open("messages.json", "r") as f:
                messages = json.load(f)
        except FileNotFoundError:
            messages = []

        messages.append(new_message)

        with open("messages.json", "w") as f:
            json.dump(messages, f, indent=4)

        return "Message sent!"
    return render_template("contact.html")

# Admin login (simple version)
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Replace with your own secret login
        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect("/dashboard")
        else:
            return "Wrong username or password"

    return render_template("admin.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect("/admin")

    try:
        with open("messages.json", "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []

    return render_template("dashboard.html", messages=messages)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
