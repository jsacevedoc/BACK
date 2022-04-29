from flask import Flask, render_template, make_response, jsonify, request
from db import count_users, get_all_users, get_user, update_email
import requests
import re

app = Flask(__name__)

PORT = 3200

# # Get Method

INFO = {
    "languages": {
        "es":"Spanish",
        "en":"English",
        "fr":"French",
    },
    "colors":{
        "r":"red",
        "g":"green",
        "b":"blue",
    },
    "clouds":{
        "IBM":"IBM CLOUD",
        "AMAZON":"AWS",
        "MICROSOFT":"AZURE",
    }
}

@app.route("/")
def home():
   print("Users count")
   print(count_users())
   print("All users")
   print(get_all_users())
   return "<h1 style='color:red'>This is home!</h1>"

@app.route('/temp')
def hello_world():
    return render_template('index.html')

@app.route("/qstr")
def qs():
    if request.args:
        req = request.args
        res = {}
        for key, value in req.items():
            res[key] = value
        res = make_response(jsonify(res), 200)
        return res

    res = make_response(jsonify({"error": "No Query String"}), 404)
    return res

@app.route("/json")
def get_json():
    res = make_response(jsonify(INFO), 200)
    return res

@app.route("/json/<collection>/<member>")   #get data with path 
def get_data(collection, member):
    print("getting the value of %s in the collection %s"%(member,collection))
    if collection in INFO:
        member = INFO[collection].get(member)
        if member:
            res = make_response(jsonify({"res":member}), 200)
            return res

        res = make_response(jsonify({"error": "Not found"}), 404)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

@app.route("/users")   #get data with path 
def get_users():
    users_list = get_all_users()

    if users_list:
        for user in users_list:
            del user['_id']
        res = make_response(jsonify({"res":users_list}), 200)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

@app.route("/users/<username>")   #get data with path 
def get_user_by_username(username):
    user = get_user(username)
    
    if user:
        del user['_id']
        res = make_response(jsonify({"res":user}), 200)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res


# Post Method

@app.route("/json/<collection>", methods=["POST"])
def create_col(collection):

    req = request.get_json()

    if collection in INFO:
        res = make_response(jsonify({"error": "Collection already exists"}), 400)
        return res

    INFO.update({collection: req})

    res = make_response(jsonify({"message": "Collection created"}), 201)
    return res

@app.route("/email/<email>", methods=["GET", "POST"])
def email_verification(email):
    if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',email.lower()):
        return make_response(jsonify({"Result":"The email has a valid syntax"}))
    else:
        return  make_response(jsonify({"Result":"The mail does not have a valid syntax"}))

# Put Method

@app.route("/newemail/<email>/<new_email>", methods=["GET", "POST","PUT"])
def put_col_mem(email,new_email):
    result = update_email(email,new_email)
    if result:
        res = make_response(jsonify({"res":"UPDATE SUCCESFULLY"}), 200)
        return res
    else:
        res = make_response(jsonify({"error": "NOT FOUND"}), 404)
        return res

# Delete Method

@app.route("/json/<collection>", methods=["DELETE"])
def delete_col(collection):

    if collection in INFO:
        del INFO[collection]
        res = make_response(jsonify(INFO), 200)
        return res

    res = make_response(jsonify({"error": "Collection not found"}), 404)
    return res

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host='0.0.0.0', port=PORT)