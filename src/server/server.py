import socket
import threading
import json

from chat.chat import Chat
from database.database import init_database

init_database()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()


def handle_client(client_socket):
    while True:
        json_data = client_socket.recv(1024).decode('utf-8')
        message = json.loads(json_data)
        print(message)

        if message['type'] == 'login':
            Chat.login(message)
        elif message['type'] == 'sign_up':
            Chat.sign_up(message.data)
        elif message['type'] == 'close_connection':
            client_socket.close()
            break


while True:
    client, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
