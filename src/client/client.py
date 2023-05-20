import socket
from pick import pick as selectMenu
from auth.auth import Auth
import os
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

while True:
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
        Auth.login(client)

    elif menu_option[1] == 1:
        Auth.sign_up(client)

    elif menu_option[1] == 2:
        client.send(
            json.dumps(
                {
                    "type": "close_connection",
                    "data": None,
                }
            ).encode("utf-8")
        )
        os.system("cls" if os.name == "nt" else "clear")
        break

client.close()
