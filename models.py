from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    hn_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(1000), nullable=True)
    points = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, nullable=True)
    date_scraped = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.hn_id}: {self.title[:50]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'hn_id': self.hn_id,
            'title': self.title,
            'link': self.link,
            'points': self.points,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_scraped': self.date_scraped.isoformat() if self.date_scraped else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None,
        }