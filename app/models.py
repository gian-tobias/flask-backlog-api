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
    activity = db.relationship("Activity", backref="user", uselist=True)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email')


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    isComplete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    episode = db.relationship("Episode", back_populates="activity", uselist=False)
 
    def __init__(self, activity_type, name, desc, user_id, episode_id=None):
        self.activity_type = activity_type
        self.name = name
        self.desc = desc
        self.user_id = user_id
        if episode_id != None:
            self.episode_id = episode_id

    def __repr__(self):
            return '<Activity %r>' % self.name

class ActivitySchema(ma.Schema):
    class Meta:
        include_fk = True
        fields = ('id', 'activity_type', 'name', 'desc', 'date_posted', 'isComplete', 'user_id', 'episode_id')

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