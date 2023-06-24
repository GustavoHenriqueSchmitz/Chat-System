import json
import secrets
import mysql.connector
from mysql.connector import errorcode


class ChatController:
    @staticmethod
    def create_chat(client_socket, database, message):
        try:
            user = database["users"].find_user(
                message["data"]["added_user_phone_number"]
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
                    chat = database["chats"].find_chat(chat_code)
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
