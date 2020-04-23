from flask import request, jsonify
from app import app, db, bcrypt, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Activity, Episode, UserSchema, ActivitySchema, EpisodeSchema
import json

user_schema = UserSchema()
users_schema = UserSchema(many=True)
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)
episode_schema = EpisodeSchema()

# Routes

# USER ROUTES

# Register user
@app.route('/register', methods=['POST'])
def register_user():
    if not request.is_json:
        return jsonify({ 'msg': 'Missing or invalid JSON request '})

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)
    # Validate request
    if username and email and password:
        # Validate duplicate username / email
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({ 'msg' : 'Duplicate username'})
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({ 'msg' : 'Duplicate email'})

        # Hash password after passing validation
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username, hashed_password, email)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)

    else:
        return jsonify({ 'msg' : 'Missing fields'})

# Login and return a JWT     
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({ 'msg': 'Missing or invalid JSON request '})

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"msg": "Missing username"})
    if not password:
        return jsonify({"msg": "Missing password"})
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = jwt._create_access_token(identity=username)
        print(user.activity)
        return jsonify(access_token)
    else:
        return jsonify({ "msg": "Invalid credentials"})

# Get specific user
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Get all users
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

# Update a user
@app.route('/user/<id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get(id)

    username = request.json.get('username', user.username)
    password = request.json.get('password', user.password)
    email = request.json.get('email', user.email)

    if password != user.password:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
    else:
        user.password = password
    
    user.username = username   
    user.email = email

    db.session.commit()
    
    return user_schema.jsonify(user)

# Delete specific user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

# ACTIVITY ROUTES

# Create new activity
# jwt_ required returns 422/401 if invalid
@app.route('/user/activity/new', methods=['POST'])
@jwt_required
def new_activity():
    if not request.is_json:
        return jsonify({ 'msg': 'Missing or invalid JSON request '})
    current_user = User.query.filter_by(username=get_jwt_identity()).first()

    activity_type = request.json.get("activity_type", None)
    name = request.json.get("name", None)
    desc = request.json.get("desc", None)
    user_id = current_user.id
    if activity_type and name and desc and user_id:
        new_activity = Activity(activity_type=activity_type, name=name, desc=desc, user_id=user_id)

        db.session.add(new_activity)
        db.session.commit()

        return activity_schema.jsonify(new_activity)
    else:
        return jsonify({ "msg": "Missing fields"})

# Get all activities
@app.route('/activity', methods=['GET'])
def get_activities():
    all_activities = Activity.query.all()
    result = activities_schema.dump(all_activities)

    return jsonify(result)

# Get all activities of a user
@app.route('/user/activity', methods=['GET'])
@jwt_required
def get_user_activities():
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    return activities_schema.jsonify(current_user.activity)

# Get a single user activity
@app.route('/user/activity/<id>', methods=['GET'])
@jwt_required
def get_user_activity(id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    # Verify user and activity
    if current_user:
        activity = Activity.query.get(id)
    if activity:
        return activity_schema.jsonify(activity)
    else:
        return jsonify({ 'msg': 'No user or activity entry'})

# Edit an activity
@app.route('/user/activity/<id>', methods=['PUT'])
@jwt_required
def edit_activity(id):
    if not request.is_json:
        return jsonify({ 'msg': 'Missing or invalid JSON request '})
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user:
        # Validate if activity exists inside user object
        for activity in current_user.activity:
            if activity.id == int(id):
                activity.activity_type = request.json.get("activity_type", activity.activity_type)
                activity.name = request.json.get("name", activity.name)
                activity.desc = request.json.get("desc", activity.desc)
                isComplete = request.json.get("isComplete", activity.isComplete)
                # Check equality with string true to return Python type Boolean
                activity.isComplete = isComplete.lower() == "true"
                return activity_schema.jsonify(activity)
        return jsonify({ 'msg': 'No activity entry'})
    else:
        return jsonify({ 'msg': 'No user entry'})

# Delete specific activity
@app.route('/activity/<id>', methods=['DELETE'])
@jwt_required
def delete_activity(id):
    activity = Activity.query.get(id)
    db.session.delete(activity)
    db.session.commit()

    return activity_schema.jsonify(activity)

# Pass activity id and add episode class
@app.route('/activity/episode/<id>', methods=['POST'])
def add_episodes(id):
    if not request.is_json:
        return jsonify({ 'msg': 'Missing or invalid JSON request '})
    # Query database for activity to verify existence
    current_activity = Activity.query.get(id)
    activity_id=current_activity.id

    episode_total = request.json.get("episode_total", 0)
    episode_progress = request.json.get("episode_progress", 0)

    if activity_id:
        new_episode = Episode(episode_total=episode_total, episode_progress=episode_progress, activity_id=activity_id)

        db.session.add(new_episode)
        db.session.commit()

        return episode_schema.jsonify(new_episode)
    else:
        return jsonify({ "msg": "Missing fields"})


