import json


class AuthController:
    @staticmethod
    def login(client_socket, database, message):
        try:
            user = database["users"].find_user(message["data"]["phone_number"])
        except:
            client_socket.send(
                json.dumps(
                    {"message": "User not found.", "data": None, "status": False}
                ).encode("utf-8")
            )
            return
        else:
            if message["data"]["password"] == user["password"]:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Login Successfully!",
                            "data": user,
                            "status": True,
                        }
                    ).encode("utf-8")
                )
                return
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Invalid Password.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return

    @staticmethod
    def sign_up(client_socket, database, message):
        try:
            database["users"].find_user(message["data"]["phone_number"])
        except:
            try:
                database["users"].create_user(
                    message["data"]["name"],
                    message["data"]["phone_number"],
                    message["data"]["password"],
                )
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Error while trying to register, try again or later.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Registered successfully!",
                            "data": None,
                            "status": True,
                        }
                    ).encode("utf-8")
                )
                return
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "This user already exists, try again or go to login.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return

    @staticmethod
    def delete_user(client_socket, database, message):
        try:
            database["users"].delete_user(message["data"])
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Failed while trying to delete user, try again or later",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "User Deleted.",
                        "data": None,
                        "status": True,
                    }
                ).encode("utf-8")
            )
