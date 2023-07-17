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
                    result = Chat.find_chats(client, user_information, "chat")
                    if result["status"] == True and result["data"] != []:
                        chats_names = []
                        for chat in result["data"]:
                            chats_names.append(chat["name"])

                        while True:
                            try:
                                menu_option = selectMenu(
                                    chats_names,
                                    "Chats | ctrl+c to return",
                                    "=>",
                                    0,
                                )
                                chat_index = menu_option[1]
                                while True:
                                    try:
                                        menu_option = selectMenu(
                                            ["Chat", "Delete Chat", "Rename Chat"],
                                            f"{chats_names[chat_index]} | ctrl+c to return",
                                            "=>",
                                            0,
                                        )
                                    except KeyboardInterrupt:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        break
                            except KeyboardInterrupt:
                                os.system("cls" if os.name == "nt" else "clear")
                                break

                elif menu_option[1] == 1:
                    result = Chat.find_chats(client, user_information, "group")
                    if result["status"] == True and result["data"] != []:
                        chats_names = []
                        for chat in result["data"]:
                            chats_names.append(chat["name"])

                        while True:
                            try:
                                menu_option = selectMenu(
                                    chats_names,
                                    "Groups | ctrl+c to return",
                                    "=>",
                                    0,
                                )
                                group_index = menu_option[1]
                                while True:
                                    try:
                                        menu_option = selectMenu(
                                            [
                                                "Chat",
                                                "Add User",
                                                "Remove User" "Delete Group",
                                                "Rename Group",
                                            ],
                                            f"{chats_names[group_index]} | ctrl+c to return",
                                            "=>",
                                            0,
                                        )
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
                                "Chat Settings",
                                "=>",
                                0,
                            )
                        except KeyboardInterrupt:
                            break

                        if menu_option[1] == 0:
                            result = User.change_name(client, user_information)

                            if result["status"] == True:
                                login_results["data"]["name"] = result["data"]

                        elif menu_option[1] == 1:
                            result = User.change_phone_number(client, user_information)

                            if result["status"] == True:
                                login_results["data"]["phone_number"] = result["data"]

                        elif menu_option[1] == 2:
                            result = User.change_password(client, user_information)

                            if result["status"] == True:
                                login_results["data"]["password"] = result["data"]

                        elif menu_option[1] == 3:
                            result = User.delete_user(client, user_information)
                            if result["status"] == True:
                                loops_breaker += 2
                            continue

    elif menu_option[1] == 1:
        Auth.sign_up(client)
