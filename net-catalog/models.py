from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default="Unknown")  # New field to track resource status

    def __repr__(self):
        return f"<Resource {self.name}>"
