from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    projects = db.relationship('Project', lazy=True)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "projects": list(map(lambda x: x.serialize(), self.projects))
        }

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    
    def __repr__(self):
        return '<Project %r>' % self.name
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }