import json
import secrets
import uuid
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
                    chat = database["chats"].find_chats(
                        user_chat["id_chat"], message["data"]["chat_type"]
                    )
                    if chat not in chats:
                        chats.append(chat)
                except database["chats"].ChatNotFoundError:
                    pass
        except:
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
            if chats != []:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Chats found with success"
                            if message["data"]["chat_type"] == "chat"
                            else "Groups found with success",
                            "data": chats,
                            "status": True,
                        }
                    ).encode("utf-8")
                )
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "No chats found"
                            if message["data"]["chat_type"] == "chat"
                            else "No groups found",
                            "data": chats,
                            "status": False,
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
                users_chats_user = database["users_chats"].find_users_chats(
                    message["data"]["user_id"], None
                )
                users_chats_added_user = database["users_chats"].find_users_chats(
                    user["id"], None
                )
                for user_chat_user in users_chats_user:
                    if (
                        database["chats"].find_chats(user_chat_user["id_chat"], None)[
                            "chat_type"
                        ]
                        == "group"
                    ):
                        continue
                    for user_chat_added_user in users_chats_added_user:
                        if user_chat_user["id_chat"] == user_chat_added_user["id_chat"]:
                            raise
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "This chat already exist.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
            else:
                try:
                    chat_id = str(uuid.uuid4())
                    database["chats"].create_chat(
                        chat_id, message["data"]["chat_name"], "chat"
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
                        chat = database["chats"].find_chats(chat_id, None)
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
                if added_user in users:
                    continue
                user = database["users"].find_users(None, added_user)
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
                chat_id = str(uuid.uuid4())
                database["chats"].create_chat(
                    chat_id, message["data"]["group_name"], "group"
                )
            except Exception as e:
                print(e)
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
                    chat = database["chats"].find_chats(chat_id, None)
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
