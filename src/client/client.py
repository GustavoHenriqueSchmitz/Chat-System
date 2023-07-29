import socket
import time
from pick import pick as selectMenu
from auth.auth import Auth
from user.user import User
from chat.chat import Chat
import os
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

while True:
    loops_breaker = 0
    os.system("cls" if os.name == "nt" else "clear")

    try:
        menu_option = selectMenu(
            [
                "Login",
                "Sign Up",
            ],
            "Chat System Login | ctrl+c to exit",
            "=>",
            0,
        )
    except KeyboardInterrupt:
        client.send(
            json.dumps(
                {
                    "request_type": "close_connection",
                    "data": None,
                }
            ).encode("utf-8")
        )
        os.system("cls" if os.name == "nt" else "clear")
        client.close()
        exit()

    if menu_option[1] == 0:
        login_results = Auth.login(client)
        user_information = login_results["data"]

        if login_results["status"] == True:
            while True:
                if loops_breaker > 0:
                    break

                try:
                    menu_option = selectMenu(
                        [
                            "Chats",
                            "Groups",
                            "Create Chat",
                            "Create Group",
                            "Settings",
                        ],
                        f"Welcome to the chat, {login_results['data']['name']}! | ctrl+c to exit",
                        "=>",
                        0,
                    )
                except KeyboardInterrupt:
                    client.send(
                        json.dumps(
                            {
                                "request_type": "close_connection",
                                "data": None,
                            }
                        ).encode("utf-8")
                    )
                    os.system("cls" if os.name == "nt" else "clear")
                    client.close()
                    exit()

                if menu_option[1] == 0:
                    chats_results = Chat.find_chats_groups(
                        client, user_information, "chat"
                    )
                    if chats_results["status"] == True and chats_results["data"] != []:
                        chats_names = []
                        for chat in chats_results["data"]:
                            chats_names.append(chat["name"])

                        while True:
                            try:
                                try:
                                    menu_option = selectMenu(
                                        chats_names,
                                        "Chats | ctrl+c to return",
                                        "=>",
                                        0,
                                    )
                                except ValueError:
                                    break
                                chat_index = menu_option[1]
                                while True:
                                    try:
                                        menu_option = selectMenu(
                                            ["Chat", "Delete Chat", "Rename Chat"],
                                            f"{chats_names[chat_index]} | ctrl+c to return",
                                            "=>",
                                            0,
                                        )
                                        if menu_option[1] == 0:
                                            pass
                                        elif menu_option[1] == 1:
                                            delete_chat_results = (
                                                Chat.delete_chat_group(
                                                    client,
                                                    chats_results["data"][chat_index][
                                                        "id"
                                                    ],
                                                    chats_results["data"][chat_index][
                                                        "chat_type"
                                                    ],
                                                )
                                            )
                                            if delete_chat_results["status"] == True:
                                                del chats_names[chat_index]
                                                del chats_results["data"][chat_index]
                                                break
                                        elif menu_option[1] == 2:
                                            rename_chat_results = (
                                                Chat.rename_chat_group(
                                                    client,
                                                    chats_results["data"][chat_index][
                                                        "id"
                                                    ],
                                                    chats_results["data"][chat_index][
                                                        "chat_type"
                                                    ],
                                                )
                                            )
                                            if rename_chat_results["status"] == True:
                                                chats_names[
                                                    chat_index
                                                ] = rename_chat_results["data"][
                                                    "new_name"
                                                ]
                                                chats_results["data"][chat_index][
                                                    "name"
                                                ] = rename_chat_results["data"][
                                                    "new_name"
                                                ]

                                    except KeyboardInterrupt:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        break
                            except KeyboardInterrupt:
                                os.system("cls" if os.name == "nt" else "clear")
                                break

                elif menu_option[1] == 1:
                    groups_results = Chat.find_chats_groups(
                        client, user_information, "group"
                    )
                    if (
                        groups_results["status"] == True
                        and groups_results["data"] != []
                    ):
                        groups_names = []
                        for chat in groups_results["data"]:
                            groups_names.append(chat["name"])

                        while True:
                            try:
                                try:
                                    menu_option = selectMenu(
                                        groups_names,
                                        "Groups | ctrl+c to return",
                                        "=>",
                                        0,
                                    )
                                except ValueError:
                                    break
                                group_index = menu_option[1]
                                while True:
                                    try:
                                        menu_option = selectMenu(
                                            [
                                                "Chat",
                                                "Add User",
                                                "Remove User",
                                                "Delete Group",
                                                "Rename Group",
                                            ],
                                            f"{groups_names[group_index]} | ctrl+c to return",
                                            "=>",
                                            0,
                                        )
                                        if menu_option[1] == 0:
                                            remove_user_results = (
                                                Chat.group_remove_user(
                                                    client,
                                                    groups_results["data"][group_index][
                                                        "id"
                                                    ],
                                                )
                                            )
                                        elif menu_option[1] == 1:
                                            add_user_results = Chat.group_add_user(
                                                client,
                                                groups_results["data"][group_index][
                                                    "id"
                                                ],
                                            )
                                        elif menu_option[1] == 2:
                                            pass
                                        elif menu_option[1] == 3:
                                            delete_group_results = (
                                                Chat.delete_chat_group(
                                                    client,
                                                    groups_results["data"][group_index][
                                                        "id"
                                                    ],
                                                    groups_results["data"][group_index][
                                                        "chat_type"
                                                    ],
                                                )
                                            )
                                            if delete_group_results["status"] == True:
                                                del groups_names[group_index]
                                                del groups_results["data"][group_index]
                                                break
                                        elif menu_option[1] == 4:
                                            rename_group_results = (
                                                Chat.rename_chat_group(
                                                    client,
                                                    groups_results["data"][group_index][
                                                        "id"
                                                    ],
                                                    groups_results["data"][group_index][
                                                        "chat_type"
                                                    ],
                                                )
                                            )
                                            if rename_group_results["status"] == True:
                                                groups_names[
                                                    group_index
                                                ] = rename_group_results["data"][
                                                    "new_name"
                                                ]
                                                groups_results["data"][group_index][
                                                    "name"
                                                ] = rename_group_results["data"][
                                                    "new_name"
                                                ]
                                    except KeyboardInterrupt:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        break
                            except KeyboardInterrupt:
                                os.system("cls" if os.name == "nt" else "clear")
                                break

                elif menu_option[1] == 2:
                    Chat.create_chat(client, user_information)

                elif menu_option[1] == 3:
                    Chat.create_group(client, user_information)

                elif menu_option[1] == 4:
                    while True:
                        if loops_breaker > 0:
                            break

                        try:
                            menu_option = selectMenu(
                                [
                                    "Change Name",
                                    "Change Number",
                                    "Change Password",
                                    "Delete User",
                                ],
                                "Chat Settings | ctrl+c to return",
                                "=>",
                                0,
                            )
                        except KeyboardInterrupt:
                            break

                        if menu_option[1] == 0:
                            change_user_name_results = User.change_name(
                                client, user_information
                            )

                            if change_user_name_results["status"] == True:
                                login_results["data"][
                                    "name"
                                ] = change_user_name_results["data"]

                        elif menu_option[1] == 1:
                            change_phone_number_results = User.change_phone_number(
                                client, user_information
                            )

                            if change_phone_number_results["status"] == True:
                                login_results["data"][
                                    "phone_number"
                                ] = change_phone_number_results["data"]

                        elif menu_option[1] == 2:
                            change_password_results = User.change_password(
                                client, user_information
                            )

                            if change_password_results["status"] == True:
                                login_results["data"][
                                    "password"
                                ] = change_password_results["data"]

                        elif menu_option[1] == 3:
                            delete_user_results = User.delete_user(
                                client, user_information
                            )
                            if delete_user_results["status"] == True:
                                loops_breaker += 2
                            continue

    elif menu_option[1] == 1:
        Auth.sign_up(client)
