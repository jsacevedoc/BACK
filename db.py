from pymongo import MongoClient

client = MongoClient("mongodb+srv://arq:admin@arq.hs1ao.mongodb.net/users_db?retryWrites=true&w=majority")

db = client.get_database('users_db')
users = db.users

def count_users():
    return users.count_documents({})

def get_all_users():
    return list(users.find())

def update_email(email,newEmail):
    try:
        myquery = { "email_address": email }
        newvalues = { "$set": { "email_address": newEmail } }
        users.update_one(myquery, newvalues)
        return True
    except:
        return False
