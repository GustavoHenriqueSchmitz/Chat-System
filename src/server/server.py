import socket
import threading
import json
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController
from controllers.chat_controller import ChatController

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
            AuthController.login(client_socket, database, message)

        elif message["request_type"] == "sign_up":
            AuthController.sign_up(client_socket, database, message)

        elif message["request_type"] == "change_user_name":
            UserController.change_name(client_socket, database, message)

        elif message["request_type"] == "change_user_phone_number":
            UserController.change_phone_number(client_socket, database, message)

        elif message["request_type"] == "change_user_password":
            UserController.change_password(client_socket, database, message)

        elif message["request_type"] == "delete_user":
            UserController.delete_user(client_socket, database, message)

        elif message["request_type"] == "find_chats_groups":
            ChatController.find_chats_groups(client_socket, database, message)

        elif message["request_type"] == "create_chat":
            ChatController.create_chat(client_socket, database, message)

        elif message["request_type"] == "create_group":
            ChatController.create_group(client_socket, database, message)

        elif message["request_type"] == "group_add_user":
            ChatController.group_add_user(client_socket, database, message)

        elif message["request_type"] == "rename_chat_group":
            ChatController.rename_chat_group(client_socket, database, message)

        elif message["request_type"] == "delete_chat_group":
            ChatController.delete_chat_group(client_socket, database, message)

        elif message["request_type"] == "close_connection":
            client_socket.close()
            break


while True:
    client, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
