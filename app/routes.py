from flask import request, jsonify
from app import app, db, bcrypt, jwt
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

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({ 'msg': 'Missing or invalid JSON request '})

    username = request.json["username"]
    password = request.json["password"]
    if not username:
        return jsonify({"msg": "Missing username"})
    if not password:
        return jsonify({"msg": "Missing password"})
    user = User.query.filter_by(username=username).first()
    print(user.password)
    print(bcrypt.check_password_hash(user.password, 'gianpassword'))
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = jwt._create_access_token(identity=username)
        return jsonify(access_token)
    else:
        return jsonify({ "msg": "Invalid credentials"})

