import json
import secrets
import mysql.connector
from mysql.connector import errorcode


class ChatController:
    @staticmethod
    def find_chats(client_socket, database, message):
        try:
            users_chats = database["users_chats"].find_users_chats(
                message["data"]["user_id"], None
            )
            chats = []
            for user_chat in users_chats:
                try:
                    chats.append(database["chats"].find_chats(user_chat["id_chat"], None, message["data"]["chat_type"]))
                except database["chats"].ChatNotFoundError:
                    pass
        except Exception as e:
            client_socket.send(
                json.dumps(
                    {
                        "message": "There was a problem while finding your chats, try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
        else:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Chats found with success",
                        "data": chats,
                        "status": True,
                    }
                ).encode("utf-8")
            )

    @staticmethod
    def create_chat(client_socket, database, message):
        try:
            user = database["users"].find_users(
                None, message["data"]["added_user_phone_number"]
            )
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "The added user not exists.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
        else:
            try:
                chats = database["chats"].find_chats()
                chat_codes = []
                for chat in chats:
                    chat_codes.append(chat["chat_code"])
                while True:
                    chat_code = secrets.token_hex(30)
                    if chat_code not in chat_codes:
                        break
                database["chats"].create_chat(
                    message["data"]["chat_name"], "chat", chat_code
                )
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Failed while trying to create the chat.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
            else:
                try:
                    chat = database["chats"].find_chats(chat_code)
                except:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Failed while trying to create the chat.",
                                "data": None,
                                "status": False,
                            }
                        ).encode("utf-8")
                    )
                else:
                    try:
                        database["users_chats"].create_user_chat(
                            message["data"]["user_id"],
                            chat["id"],
                        )
                        database["users_chats"].create_user_chat(
                            user["id"],
                            chat["id"],
                        )
                    except mysql.connector.Error as error:
                        if error.errno == errorcode.ER_DUP_ENTRY:
                            client_socket.send(
                                json.dumps(
                                    {
                                        "message": "This chat already exists, try another.",
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
                                        "message": "Error while trying to create chat, try again or later.",
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
                                    "message": "Chat created with success",
                                    "data": None,
                                    "status": True,
                                }
                            ).encode("utf-8")
                        )
                        return

    @staticmethod
    def create_group(client_socket, database, message):
        try:
            users = []
            for added_user in message["data"]["added_users_phone_number"]:
                user = database["users"].find_users(
                    None, added_user
                )
                users.append(user)
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Some added user doesn`t exist",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
        else:
            try:
                chats = database["chats"].find_chats()
                chat_codes = []
                for chat in chats:
                    chat_codes.append(chat["chat_code"])
                while True:
                    chat_code = secrets.token_hex(30)
                    if chat_code not in chat_codes:
                        break
                database["chats"].create_chat(
                    message["data"]["group_name"], "group", chat_code
                )
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Failed while trying to create the group.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
            else:
                try:
                    chat = database["chats"].find_chats(chat_code=chat_code)
                except:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Failed while trying to create the group.",
                                "data": None,
                                "status": False,
                            }
                        ).encode("utf-8")
                    )
                else:
                    try:
                        database["users_chats"].create_user_chat(
                            message["data"]["user_id"],
                            chat["id"],
                        )
                        for user in users:
                            database["users_chats"].create_user_chat(
                                user["id"],
                                chat["id"],
                            )
                    except mysql.connector.Error as error:
                        if error.errno == errorcode.ER_DUP_ENTRY:
                            client_socket.send(
                                json.dumps(
                                    {
                                        "message": "This group already exists, try another.",
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
                                        "message": "Error while trying to create group, try again or later.",
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
                                    "message": "Group created with success",
                                    "data": None,
                                    "status": True,
                                }
                            ).encode("utf-8")
                        )
                        return
