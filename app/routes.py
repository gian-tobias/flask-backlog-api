from flask import request, jsonify
from app import app, db, bcrypt, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Activity, Episode, UserSchema, ActivitySchema, EpisodeSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)
episode_schema = EpisodeSchema()
# Routes

# Register user
@app.route('/register', methods=['POST'])
def register_user():
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
            return jsonify({ 'msg' : 'Duplicate username'})

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
    print(user.activity)
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = jwt._create_access_token(identity=username)
        return jsonify(access_token)
    else:
        return jsonify({ "msg": "Invalid credentials"})

# Get specific user

# Get all users
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

# Delete specific user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


# Create new activity
# jwt_ required returns 422/401 if invalid
@app.route('/activity/new', methods=['POST'])
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

# Delete specific activity
@app.route('/activity/<id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    db.session.delete(activity)
    db.session.commit()

    return activity_schema.jsonify(activity)

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