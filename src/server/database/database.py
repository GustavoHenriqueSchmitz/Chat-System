import threading
import time
from mysql.connector import connect
from .models.chats import Chats
from .models.messages import Messages
from .models.users_chats import UsersChats
from .models.users import Users


def check_connection_status(connection):
    while True:
        if not connection.is_connected():
            print("Database connection failed. Reconnecting...")
            try:
                connection.reconnect()
            except:
                print("Error while trying to reconnect, trying again...")
            else:
                print("Reconnected!")
        time.sleep(5)


def init_database():
    connection = connect(
        host="localhost",
        user="root",
        password="root",
        database="Chat-System",
        port="3306",
    )
    connection_status_thread = threading.Thread(
        target=check_connection_status, args=(connection,)
    )
    connection_status_thread.start()

    database = {
        "users": Users(connection),
        "chats": Chats(connection),
        "messages": Messages(connection),
        "users_chats": UsersChats(connection),
    }
    return database
