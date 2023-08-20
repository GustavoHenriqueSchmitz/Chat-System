import json
import uuid
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


class ChatController:
    @staticmethod
    def find_chats_groups(client_socket, database, message):
        try:
            users_chats_results = database["users_chats"].find_users_chats(
                {
                    "where": {"id_user": message["data"]["user_id"]},
                    "join": {
                        "chats": {"join_type": "right", "on_condition": "chats.id"}
                    },
                }
            )
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": f"There was a problem while finding your {'chats' if message['data']['type'] == 'chat' else 'groups'}, try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return {"status": False, "data": None}
        else:
            try:
                chats = []
                for chat in users_chats_results:
                    if (
                        chat["chat_type"] == message["data"]["type"]
                        and chat not in chats
                    ):
                        chats.append(chat)
                if chats != []:
                    for chat in chats:
                        chat_users = database["users_chats"].find_users_chats(
                            {
                                "where": {"id_chat": chat["id"]},
                                "join": {"users": {"on_condition": "users.id"}},
                            }
                        )
                        chat["users"] = [
                            {
                                "id": chat_user["id"],
                                "name": chat_user["name"],
                                "phone_number": chat_user["phone_number"],
                            }
                            for chat_user in chat_users
                        ]
                    client_socket.send(
                        json.dumps(
                            {
                                "message": f"{'Chats' if message['data']['type'] == 'chat' else 'Groups'} found with success",
                                "data": chats,
                                "status": True,
                            }
                        ).encode("utf-8")
                    )
                else:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": f"No {'chats' if message['data']['type'] == 'chat' else 'groups'} found",
                                "data": chats,
                                "status": False,
                            }
                        ).encode("utf-8")
                    )
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": f"There was a problem while finding your {'chats' if message['data']['type'] == 'chat' else 'groups'}, try again or later.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {"status": False, "data": None}

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
            return {"status": False, "data": None}
        else:
            try:
                users_chats_user = database["users_chats"].find_users_chats(
                    {"where": {"id_user": message["data"]["user_id"]}}
                )
                users_chats_added_user = database["users_chats"].find_users_chats(
                    {"where": {"id_user": user["id"]}}
                )
                for user_chat_user in users_chats_user:
                    counter = 0
                    if (
                        database["chats"].find_chats(user_chat_user["id_chat"], None)[
                            "chat_type"
                        ]
                        == "group"
                    ):
                        continue
                    else:
                        for user_chat_added_user in users_chats_added_user:
                            if (
                                database["chats"].find_chats(
                                    user_chat_user["id_chat"], None
                                )["chat_type"]
                                == "group"
                            ):
                                continue
                            else:
                                if (
                                    user_chat_user["id_chat"]
                                    == user_chat_added_user["id_chat"]
                                ):
                                    if (
                                        user_chat_user["id_user"]
                                        != user_chat_added_user["id_user"]
                                    ):
                                        raise
                                    else:
                                        counter += 1
                                        if counter >= 2:
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
                return {"status": False, "data": None}
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
                    return {"status": False, "data": None}
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
                        return {"status": False, "data": None}
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
                                return {"status": False, "data": None}
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
                                return {"status": False, "data": None}
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
                            return {"status": True, "data": None}

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
            return {"status": False, "data": None}
        else:
            try:
                chat_id = str(uuid.uuid4())
                database["chats"].create_chat(
                    chat_id, message["data"]["group_name"], "group"
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
                return {"status": False, "data": None}
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
                    return {"status": False, "data": None}
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
                            return {"status": False, "data": None}
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
                            return {"status": False, "data": None}
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
                        return {"status": True, "data": None}

    @staticmethod
    def delete_chat_group(client_socket, database, message):
        try:
            database["users_chats"].delete_user_chat(None, None, message["data"]["id"])
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": f"There was an error while trying to delete your {'chat' if message['data']['type'] == 'chat' else 'group'}, try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return {"status": False, "data": None}
        else:
            try:
                database["chats"].delete_chat(message["data"]["id"])
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": f"There was an error while trying to delete your {'chat' if message['data']['type'] == 'chat' else 'group'}, try again or later.",
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
                            "message": f"{'Chat' if message['data']['type'] == 'chat' else 'Group'} deleted with success!",
                            "data": None,
                            "status": True,
                        }
                    ).encode("utf-8")
                )
                return {"status": True, "data": None}

    @staticmethod
    def rename_chat_group(client_socket, database, message):
        try:
            database["chats"].update_chat(
                message["data"]["id"], message["data"]["new_name"], None
            )
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": f"There was an error while trying to rename your {'chat' if message['data']['type'] == 'chat' else 'group'}, try again or later.",
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
                        "message": f"{'Chat' if message['data']['type'] == 'chat' else 'Group'} renamed with success!",
                        "data": {"new_name": message["data"]["new_name"]},
                        "status": True,
                    }
                ).encode("utf-8")
            )
            return {"status": True, "data": None}

    @staticmethod
    def group_add_user(client_socket, database, message):
        try:
            user = database["users"].find_users(None, message["data"]["added_user"])
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
            return {"status": False, "data": None}
        else:
            try:
                group_users_chats = database["users_chats"].find_users_chats(
                    {"where": {"id_chat": message["data"]["group_id"]}}
                )
                for group_user_chat in group_users_chats:
                    if group_user_chat["id_user"] == user["id"]:
                        raise
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "This user is already added.",
                            "data": None,
                            "status": False,
                        }
                    ).encode("utf-8")
                )
                return {"status": True, "data": None}
            else:
                try:
                    database["users_chats"].create_user_chat(
                        user["id"], message["data"]["group_id"]
                    )
                except:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Error trying to add user, please try again or later.",
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
                                "message": "User added with success.",
                                "data": {"user_information": user},
                                "status": True,
                            }
                        ).encode("utf-8")
                    )
                    return {"status": True, "data": None}

    @staticmethod
    def group_remove_user(client_socket, database, message):
        try:
            group_user_ligations = database["users_chats"].find_users_chats(
                {"where": {"id_chat": message["data"]["group_id"]}}
            )
            database["users_chats"].delete_user_chat(
                None, message["data"]["user_id"], message["data"]["group_id"]
            )
            if len(group_user_ligations) <= 1:
                database["chats"].delete_chat(message["data"]["group_id"])
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Error trying to remove user, please try again or later.",
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
                        "message": "User removed with success.",
                        "data": None,
                        "status": True,
                    }
                ).encode("utf-8")
            )
            return {"status": True, "data": None}

    @staticmethod
    def chat(client_socket, database, message, clients_connected):
        try:
            database["messages"].create_message(
                message["data"]["message"],
                message["data"]["sender_id"],
                message["data"]["chat_id"],
                datetime.now(),
            )
        except:
            client_socket.send(
                json.dumps(
                    {
                        "message": "Error trying to send your message, please try again or later.",
                        "data": None,
                        "status": False,
                    }
                ).encode("utf-8")
            )
            return {"status": False, "data": None}
        else:
            for user in message["data"]["chat_users"]:
                try:
                    if user["id"] != message["data"]["sender_id"]:
                        clients_connected[user["id"]].send(
                            json.dumps(
                                {
                                    "message": "",
                                    "data": {
                                        "message": message["data"]["message"],
                                        "from": message["data"]["sender_name"],
                                    },
                                    "status": True,
                                }
                            ).encode("utf-8")
                        )
                except KeyError:
                    pass
            return {"status": True, "data": None}