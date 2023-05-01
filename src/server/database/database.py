from mysql.connector import connect
from models.chats import chats
from models.messages import messages
from models.users_chats import users_chats
from models.users import users

connection = connect(
    host="localhost",
    user="root",
    password="root",
    database="Chat-System"
)

users = users(connection)
chats = chats(connection)
messages = messages(connection)
users_chats = users_chats(connection)
