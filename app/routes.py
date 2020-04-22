from flask import request, jsonify
from app import app, db, bcrypt
from app.models import User, Activity, ActivityTypeEnum, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Routes

# Register user
@app.route('/user', methods=['POST'])
def register_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    new_user = User(username, password, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)