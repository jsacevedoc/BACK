import re
import db

def is_phone_number_valid(phone_number):
    if( re.match('^([0-9]{10})|(123)$', phone_number) ):
        return True
    
    return False

def validate_user(user, password):
    print(user)
    if user["password"] == password:
        return True
    
    return False
