import json
import mysql.connector
from mysql.connector import errorcode

class AuthController:
    @staticmethod
    def login(client_socket, database, message):
        try:
            user = database["users"].find_users(None, message["data"]["phone_number"])
        except:
            client_socket.send(
                json.dumps(
                    {"message": "User not found.", "data": None, "status": False}
                ).encode("utf-8")
            )
            return {"status": False, "data": None}
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
                return {"status": True, "data": user}
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Invalid Password!",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {"status": False, "data": None}

    @staticmethod
    def sign_up(client_socket, database, message):
        try:
            database["users"].create_user(
                message["data"]["name"],
                message["data"]["phone_number"],
                message["data"]["password"],
            )
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "This user already exists, try another.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {"status": False, "data": None}
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Error while trying to register, try again or later.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {"status": False, "data": None}
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
            return {"status": True, "data": None}
