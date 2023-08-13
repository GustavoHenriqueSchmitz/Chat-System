import json
import mysql.connector
from mysql.connector import errorcode


class UserController:
    @staticmethod
    def change_name(client_socket, database, message):
        try:
            database["users"].update_user(
                message["data"]["phone_number"], None, message["data"]["new_name"], None
            )
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Failed while trying to change your name, try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return {
                "status": False,
                "data": None
            }
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Name Changed!",
                        "data": message["data"]["new_name"],
                        "status": True,
                    }
                ).encode("utf-8")
            )
            return {
                "status": True,
                "data": None
            }

    @staticmethod
    def change_phone_number(client_socket, database, message):
        try:
            database["users"].update_user(
                message["data"]["phone_number"],
                message["data"]["new_phone_number"],
                None,
                None,
            )
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "This phone number is already used, try another.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {
                    "status": False,
                    "data": None
                }
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Error while trying to change phone number, try again or later.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {
                    "status": False,
                    "data": None
                }
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Phone Number Changed!",
                        "data": message["data"]["new_phone_number"],
                        "status": True,
                    }
                ).encode("utf-8")
            )
            return {
                "status": True,
                "data": None
            }

    @staticmethod
    def change_password(client_socket, database, message):
        try:
            database["users"].update_user(
                message["data"]["phone_number"],
                None,
                None,
                message["data"]["new_password"],
            )
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Error while trying to change password, try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return {
                "status": False,
                "data": None
            }
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Password Changed!",
                        "data": message["data"]["new_password"],
                        "status": True,
                    }
                ).encode("utf-8")
            )
            return {
                "status": True,
                "data": None
            }

    @staticmethod
    def delete_user(client_socket, database, message):
        try:
            database["users"].delete_user(message["data"])
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Failed while trying to delete user, try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return {
                "status": False,
                "data": None
            }
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "User Deleted!",
                        "data": None,
                        "status": True,
                    }
                ).encode("utf-8")
            )
            return {
                "status": True,
                "data": None
            }
