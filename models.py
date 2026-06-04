from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class StandupPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    yesterday = db.Column(db.Text, nullable=False)
    today = db.Column(db.Text, nullable=False)
    blockers = db.Column(db.Text)
    has_blocker = db.Column(db.Boolean, default=False)
    file_attachment = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):

        return {
            "id": self.id,
            "author": self.author,
            "yesterday": self.yesterday,
            "today": self.today,
            "blockers": self.blockers,
            "has_blocker": self.has_blocker,
            "file_attachment": self.file_attachment,
            "timestamp": self.timestamp.isoformat()
        }