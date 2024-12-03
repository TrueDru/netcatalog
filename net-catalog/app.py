import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from models import db, Resource

app = Flask(__name__)

# Load database configuration from individual environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER', 'username')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'resources_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Ensure tables are created only if they do not exist
with app.app_context():
    db.create_all()

# Route for the main page
@app.route("/")
def index():
    resources = Resource.query.all()
    return render_template("index.html", resources=resources)

# Route to check the availability of a resource
@app.route("/check/<int:id>")
def check_resource(id):
    resource = Resource.query.get_or_404(id)
    try:
        response = requests.get(resource.url, timeout=5)
        resource.status = "Available" if response.status_code == 200 else "Unavailable"
    except Exception as e:
        resource.status = "Unavailable"
    db.session.commit()
    return redirect(url_for("index"))

# Route to add a new resource
@app.route("/add", methods=["POST"])
def add_resource():
    name = request.form.get("name")
    url = request.form.get("url")
    description = request.form.get("description")
    if name and url:
        new_resource = Resource(name=name, url=url, description=description)
        db.session.add(new_resource)
        db.session.commit()
    return redirect(url_for("index"))

# Route to delete an existing resource
@app.route("/delete/<int:id>")
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for("index"))

# Route to edit an existing resource
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_resource(id):
    resource = Resource.query.get_or_404(id)
    if request.method == "POST":
        resource.name = request.form.get("name")
        resource.url = request.form.get("url")
        resource.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", resource=resource)

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=debug)
