from werkzeug.security import check_password_hash

class User:

    def __init__(self, user_name, password, phone_number, email_address):
        self.user_name = user_name
        self.password = password
        self.phone_number = phone_number
        self.email_address = email_address

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.user_name

    def get_phone_number(self):
        return self.phone_number

    def get_email_address(self):
        return self.email_address


    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)