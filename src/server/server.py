import socket
import threading
import json

from database.database import init_database
from chat.chat import Chat

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
database = init_database()
server.listen()


def handle_client(client_socket):
    while True:
        json_data = client_socket.recv(1024).decode('utf-8')
        message = json.loads(json_data)

        if message['type'] == 'login':
            Chat.login(database, message['data'])
        elif message['type'] == 'sign_up':
            Chat.sign_up(database, message['data'])
        elif message['type'] == 'close_connection':
            client_socket.close()
            break


while True:
    client, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
