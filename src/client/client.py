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
            "Leave Program",
        ],
        "Seja bem Vindo ao Chat",
        "=>",
        0,
    )

    if menu_option[1] == 0:
        login_results = Auth.login(client)
        user_information = login_results["data"]

        if login_results["error"] == False:
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
                    "Chat Options",
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
                                "Delete User",
                                "Return",
                            ],
                            "Chat Settings",
                            "=>",
                            0,
                        )

                        if menu_option[1] == 0:
                            pass

                        elif menu_option[1] == 1:
                            while True:
                                confirm_deletion = str(input("Do you really want to delete your user? [Y/N]: ")).strip().lower()
                                if confirm_deletion != "y" and confirm_deletion != "n":
                                    print("Invalid option, digit [Y/N]")
                                    time.sleep(2)
                                    continue
                                else:
                                    break
                            
                            if confirm_deletion == "y":
                                client.send(
                                    json.dumps(
                                        {
                                            "request_type": "delete_user",
                                            "data": user_information["phone_number"]
                                        }
                                    ).encode("utf-8")
                                )
                                results = json.loads(client.recv(1024).decode("utf-8"))
                                print("------------------------------------------------")
                                print(results["message"])
                                time.sleep(3)
                                loops_breaker += 2

                            else:
                                continue

                        elif menu_option[1] == 2:
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
