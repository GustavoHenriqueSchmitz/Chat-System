class Chat():
    @staticmethod
    def login(database, data):
        pass

    @staticmethod
    def sign_up(database, user_data):
        database['users'].create_user(
            user_data['name'], user_data['phone_number'], user_data['password'])
