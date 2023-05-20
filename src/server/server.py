import socket
import threading
import json
import time

from database.database import init_database

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
database = init_database()
server.listen()


def handle_client(client_socket):
    while True:
        json_data = client_socket.recv(1024).decode("utf-8")
        message = json.loads(json_data)

        if message["type"] == "login":
            try:
                user = database["users"].find_user(message["data"]["phone_number"])
            except:
                client_socket.send(json.dumps("User not found.").encode("utf-8"))
            else:
                if message["data"]["password"] == user[2]:
                    client_socket.send(
                        json.dumps("Login Successfully!").encode("utf-8")
                    )
                else:
                    client_socket.send(json.dumps("Invalid Password.").encode("utf-8"))

        elif message["type"] == "sign_up":
            try:
                database["users"].create_user(
                    message["data"]["name"],
                    message["data"]["phone_number"],
                    message["data"]["password"],
                )
            except:
                client_socket.send(
                    json.dumps(
                        "Error while trying to register, try again or later."
                    ).encode("utf-8")
                )
            else:
                client_socket.send(
                    json.dumps("Registered successfully!").encode("utf-8")
                )
        elif message["type"] == "close_connection":
            client_socket.close()
            break


while True:
    client, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
