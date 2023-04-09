from mysql.connector import connect
from models.chats import chats
from models.messages import messages
from models.users_chats import users_chats
from models.users import users

connection = connect (
    host="localhost",
    user="root",
    password="root",
)

users(connection)
messages(connection)
users_chats(connection)
chats(connection)
