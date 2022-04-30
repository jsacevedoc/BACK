import re

def is_phone_number_valid(phone_number):
    if( re.match('^([0-9]{10})|(123)$', phone_number) ):
        return True
    
    return False
