import socket
import threading
import json
from controllers.auth_controller import AuthController

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
            AuthController.change_name(client_socket, database, message)
        
        elif message["request_type"] == "change_user_phone_number":
            AuthController.change_phone_number(client_socket, database, message)
        
        elif message["request_type"] == "change_user_password":
            AuthController.change_password(client_socket, database, message)

        elif message["request_type"] == "delete_user":
            AuthController.delete_user(client_socket, database, message)

        elif message["request_type"] == "close_connection":
            client_socket.close()
            break


while True:
    client, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
