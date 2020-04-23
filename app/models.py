from app import db, ma
from marshmallow import fields
import enum
from datetime import datetime

# User class

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    activity = db.relationship("Activity", back_populates="user", uselist=True)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# Activity class

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    isComplete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="activity")
    episode = db.relationship("Episode", back_populates="activity", uselist=False)
 
    def __init__(self, activity_type, name, desc, user_id):
        self.activity_type = activity_type
        self.name = name
        self.desc = desc
        self.user_id = user_id

    def __repr__(self):
            return '<Activity %r>' % self.name

# Episode class

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_total = db.Column(db.Integer, nullable=False)
    episode_progress = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), unique=True)
    activity = db.relationship("Activity", back_populates="episode")
    
class EpisodeSchema(ma.Schema):
    class Meta:
        include_fk = True
        fields = ('id', 'episode_total', 'episode_progress', 'activity_id')

# Include relationship schemas in serialization
# Declaration of nested schema should precede parent schema 

class ActivitySchema(ma.Schema):
    episode = fields.Nested(EpisodeSchema)
    class Meta:
        include_fk = True
        fields = ('id', 'activity_type', 'name', 'desc', 'date_posted', 'isComplete', 'user_id', 'episode')

# Activity Schema is one-to-many; invoke fields.List to serialize properly

class UserSchema(ma.Schema):
    activity = fields.List(fields.Nested(ActivitySchema))
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'activity')
        