import socket
import time
from pick import pick as selectMenu
from auth.auth import Auth
import os
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

while True:
    loops_breaker = 0
    os.system("cls" if os.name == "nt" else "clear")
    menu_option = selectMenu(
        [
            "Login",
            "Sign Up",
            "Exit chat",
        ],
        "Chat System Login",
        "=>",
        0,
    )

    if menu_option[1] == 0:
        login_results = Auth.login(client)
        user_information = login_results["data"]

        if login_results["status"] == True:
            while True:
                if loops_breaker > 0:
                    break

                menu_option = selectMenu(
                    [
                        "Chats",
                        "Groups",
                        "Create Chat",
                        "Create Group",
                        "Settings",
                        "Exit Chat",
                    ],
                    f"Welcome to the chat, {login_results['data']['name']}!",
                    "=>",
                    0,
                )

                if menu_option[1] == 0:
                    pass

                elif menu_option[1] == 1:
                    pass

                elif menu_option[1] == 2:
                    pass

                elif menu_option[1] == 3:
                    pass

                elif menu_option[1] == 4:
                    while True:
                        if loops_breaker > 0:
                            break

                        menu_option = selectMenu(
                            [
                                "Change Name",
                                "Change Number",
                                "Change Password",
                                "Delete User",
                                "Return",
                            ],
                            "Chat Settings",
                            "=>",
                            0,
                        )

                        if menu_option[1] == 0:
                            result = Auth.change_name(client, user_information)

                            if result["status"] == True:
                                login_results["data"]["name"] = result["data"]

                        elif menu_option[1] == 1:
                            result = Auth.change_phone_number(client, user_information)

                            if result["status"] == True:
                                login_results["data"]["phone_number"] = result["data"]

                        elif menu_option[1] == 2:
                            result = Auth.change_password(client, user_information)

                            if result["status"] == True:
                                login_results["data"]["password"] = result["data"]

                        elif menu_option[1] == 3:
                            result = Auth.delete_user(client, user_information)
                            if result["status"] == True:
                                loops_breaker += 2
                            continue

                        elif menu_option[1] == 4:
                            break

                elif menu_option[1] == 5:
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

    elif menu_option[1] == 1:
        Auth.sign_up(client)

    elif menu_option[1] == 2:
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
