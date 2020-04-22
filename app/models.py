from app import db, ma
import enum
from datetime import datetime

# User class

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    activities = db.relationship('Activity', backref='author', lazy=True)

    def __init__(self, username, password, email, activities=None):
        self.username = username
        self.password = password
        self.email = email
        if activities is not None:
            self.activites = activities

    def __repr__(self):
        return '<User %r>' % self.username

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'activities')

# Populate with new_activity.activity_type = ActivityTypeEnum.movie
class ActivityTypeEnum(enum.Enum):
    movie = 'movie'
    television = 'television'

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(
        db.Enum(ActivityTypeEnum),
        default=ActivityTypeEnum.movie,
        nullable=False
    )
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    isComplete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
            return '<Activity %r>' % self.name
