from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SpeechPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    speecher = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    ppt_file = db.Column(db.String(300), nullable=False)

class RecommendedPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    discussed = db.Column(db.Boolean, default=False)

