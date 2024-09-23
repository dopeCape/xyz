
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import jwt
from functools import wraps
import re
import random
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)
# JWT Secret
JWT_SECRET = "Swaraj"

# MongoDB connection
client = MongoClient(
    'mongodb+srv://swaraj:Swaraj2004@cluster0.txvw2vk.mongodb.net/PayTm-Clone')
db = client['PayTm-Clone']
users_collection = db['user']
accounts_collection = db['account']

# Authentication middleware


def auth_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]
        print(token)
        if not token:
            return jsonify({'message': 'Unauthorized'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[
                              "HS256"])  # Specify algorithms
            request.user_id = data['userId']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function
# Basic email validation


def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

# Signup route


@app.route('/api/v1/user/signup', methods=['POST'])
def signup():
    body = request.json

    # Manual validation
    if not body.get('username') or not is_valid_email(body['username']):
        return jsonify({'message': 'Invalid email'}), 400
    if not body.get('firstName'):
        return jsonify({'message': 'First name is required'}), 400
    if not body.get('lastName'):
        return jsonify({'message': 'Last name is required'}), 400
    if not body.get('password'):
        return jsonify({'message': 'Password is required'}), 400

    # Check if the user already exists
    if users_collection.find_one({'username': body['username']}):
        return jsonify({'message': 'User already exists'}), 411

    # Create the user
    user_id = users_collection.insert_one({
        'username': body['username'],
        'firstName': body['firstName'],
        'lastName': body['lastName'],
        'password': body['password']
    }).inserted_id

    # Create an account with a random balance
    accounts_collection.insert_one({
        'userId': user_id,
        'balance': 1 + random.random() * 10000
    })

    # Generate a JWT token
    token = jwt.encode({'userId': str(user_id)}, JWT_SECRET, algorithm="HS256")
    return jsonify({'message': 'User created successfully', 'token': token})

# Signin route


@app.route('/api/v1/user/signin', methods=['POST'])
def signin():
    body = request.json

    # Manual validation
    if not body.get('username') or not is_valid_email(body['username']):
        return jsonify({'message': 'Invalid email or password'}), 400
    if not body.get('password'):
        return jsonify({'message': 'Password is required'}), 400

    # Check user credentials
    user = users_collection.find_one(
        {'username': body['username'], 'password': body['password']})
    if user:
        token = jwt.encode(
            {'userId': str(user['_id'])}, JWT_SECRET, algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'message': 'Error while logging in'}), 411

# Update user info route


@app.route('/api/v1/user/update', methods=['PUT'])
@auth_middleware
def update_user():
    body = request.json

    # Only update fields that are present in the request
    updates = {}
    if body.get('password'):
        updates['password'] = body['password']
    if body.get('first_name'):
        updates['first_name'] = body['first_name']
    if body.get('last_name'):
        updates['last_name'] = body['last_name']

    # If no valid fields were provided
    if not updates:
        return jsonify({'message': 'No valid fields to update'}), 400

    # Update the user
    users_collection.update_one(
        {'_id': ObjectId(request.user_id)}, {'$set': updates})
    return jsonify({'message': 'Updated successfully'})

# Bulk search users route


@app.route('/api/v1/user/bulk', methods=['GET'])
def bulk_users():
    filter_value = request.args.get('filter', "")
    users = users_collection.find({
        '$or': [
            {'firstName': {'$regex': filter_value}},
            {'lastName': {'$regex': filter_value}}
        ]
    })

    result = [{
        'username': user['username'],
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        '_id': str(user['_id'])
    } for user in users]

    return jsonify({'users': result})

# Account balance route


@app.route('/api/v1/account/balance', methods=['GET'])
@auth_middleware
def get_balance():
    account = accounts_collection.find_one(
        {'userId': ObjectId(request.user_id)})
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    return jsonify({'balance': account['balance']})

# Transfer route


@app.route('/api/v1/account/transfer', methods=['POST'])
@auth_middleware
def transfer():
    session = client.start_session()
    session.start_transaction()

    try:
        data = request.json
        amount = int(data['amount'])
        to_user_id = data['to']

        # Check sender's account
        sender_account = accounts_collection.find_one(
            {'userId': ObjectId(request.user_id)}, session=session)
        if not sender_account or sender_account['balance'] < amount:
            session.abort_transaction()
            return jsonify({'message': 'Insufficient balance'}), 400

        # Check recipient's account
        receiver_account = accounts_collection.find_one(
            {'userId': ObjectId(to_user_id)}, session=session)
        if not receiver_account:
            session.abort_transaction()
            return jsonify({'message': 'Invalid account'}), 400

        # Update balances
        accounts_collection.update_one({'userId': ObjectId(request.user_id)}, {
                                       '$inc': {'balance': -amount}}, session=session)
        accounts_collection.update_one({'userId': ObjectId(to_user_id)}, {
                                       '$inc': {'balance': amount}}, session=session)

        session.commit_transaction()
        return jsonify({'message': 'Transfer successful'})
    except Exception as e:
        session.abort_transaction()
        return jsonify({'error': str(e)}), 500
    finally:
        session.end_session()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
