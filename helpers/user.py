import re

def phone_validation(phone_number):
    if( re.match('^([0-9]{10})|(123)$', phone_number) ):
        return True
    
    return False
