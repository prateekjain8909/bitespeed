from datetime import datetime
from database import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(20))
    email = db.Column(db.String(120))
    linkedId = db.Column(db.Integer, db.ForeignKey('contact.id'))
    linkPrecedence = db.Column(db.String(20))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    deletedAt = db.Column(db.DateTime, nullable=True)

    def __init__(self, phoneNumber=None, email=None, linkedId=None, linkPrecedence=None):
        self.phoneNumber = phoneNumber
        self.email = email
        self.linkedId = linkedId
        self.linkPrecedence = linkPrecedence

    def __eq__(self, other):
        if isinstance(other, Contact):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
