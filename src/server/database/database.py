from mysql.connector import connect
from .models.chats import Chats
from .models.messages import Messages
from .models.users_chats import UsersChats
from .models.users import Users

database = {}

def init_database():
    global database
    
    connection = connect(
        host="localhost",
        user="root",
        password="root",
        database="Chat-System"
    )

    database = {
        "users": Users(connection),
        "chats": Chats(connection),
        "messages": Messages(connection),
        "user_chats": UsersChats(connection)
    }
