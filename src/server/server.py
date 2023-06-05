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

        if message["request_type"] == "login":
            try:
                user = database["users"].find_user(message["data"]["phone_number"])
            except:
                client_socket.send(
                    json.dumps(
                        {"message": "User not found.", "data": None, "error": True}
                    ).encode("utf-8")
                )
            else:
                if message["data"]["password"] == user["password"]:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Login Successfully!",
                                "data": user,
                                "error": False,
                            }
                        ).encode("utf-8")
                    )
                else:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Invalid Password.",
                                "data": None,
                                "error": True,
                            }
                        ).encode("utf-8")
                    )

        elif message["request_type"] == "sign_up":
            try:
                database["users"].find_user(message["data"]["phone_number"])
            except:
                try:
                    database["users"].create_user(
                        message["data"]["name"],
                        message["data"]["phone_number"],
                        message["data"]["password"],
                    )
                except:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Error while trying to register, try again or later.",
                                "data": None,
                                "error": True,
                            }
                        ).encode("utf-8")
                    )
                else:
                    client_socket.send(
                        json.dumps(
                            {
                                "message": "Registered successfully!",
                                "data": None,
                                "error": False,
                            }
                        ).encode("utf-8")
                    )
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "This user already exists, try again or go to login.",
                            "data": None,
                            "error": False,
                        }
                    ).encode("utf-8")
                )
        elif message["request_type"] == "close_connection":
            client_socket.close()
            break
            
        elif message["request_type"] == "delete_user":
            try:
                database["users"].delete_user(
                    message["data"]
                )
            except:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "Failed while trying to delete user, try again or later",
                            "data": None,
                            "error": True,
                        }
                    ).encode("utf-8")
                )
            else:
                client_socket.send(
                    json.dumps(
                        {
                            "message": "User Deleted.",
                            "data": None,
                            "error": False,
                        }
                    ).encode("utf-8")
                )

while True:
    client, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
