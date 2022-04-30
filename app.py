from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS, cross_origin
from db import count_users, get_all_users, get_user, update_email, update_phone_number
import requests
import re

from helpers.user import is_phone_number_valid, validate_user

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

PORT = 3200

# Get Methods 

@app.route("/users")  
def get_users():
    users_list = get_all_users()

    if users_list:
        for user in users_list:
            del user['_id']
            del user['password']
        res = make_response(jsonify({"res":users_list}), 200)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

@app.route("/users/<username>") 
def get_user_by_username(username):
    user = get_user(username)
    
    if user:
        del user['_id']
        del user['password']
        res = make_response(jsonify({"res":user}), 200)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

@app.route("/users/sign-in/<username>/<password>") 
@cross_origin()
def sign_in(username, password):
    user = get_user(username)

    if user:
        del user['_id'] 
    else:
        return make_response(jsonify({"error": "User not found"}), 404)

    is_valid = validate_user(user, password)

    if is_valid:
        return  make_response(jsonify({"access_token":hash(user["user_name"])}), 200)
    
    return make_response(jsonify({"error": "Username and password don't match"}), 404)


# Post Methods

@app.route("/email/<email>", methods=["GET", "POST"])
def email_verification(email):
    if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',email.lower()):
        return make_response(jsonify({"Result":"The email has a valid syntax"}))
    else:
        return  make_response(jsonify({"Result":"The mail does not have a valid syntax"}))

# Put Methods

@app.route("/newemail/<email>/<new_email>", methods=["GET", "POST","PUT"])
def email_update(email,new_email):
    result = update_email(email,new_email)
    if result:
        res = make_response(jsonify({"res":"UPDATE SUCCESFULLY"}), 200)
        return res
    else:
        res = make_response(jsonify({"error": "NOT FOUND"}), 404)
        return res

@app.route("/<username>/phone_number", methods=["PUT"])
@cross_origin()
def update_phone(username):
    new_number = request.json['phone_number']

    if is_phone_number_valid(new_number):
        result = update_phone_number(username, new_number)
        if result:
            res = make_response(jsonify({}), 200)
        else:
            res = make_response(jsonify({}), 400)
    else:
        res = make_response(jsonify({}), 404)

    return res
