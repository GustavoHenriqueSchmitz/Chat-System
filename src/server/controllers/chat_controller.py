import json
import mysql.connector
from mysql.connector import errorcode

class ChatController:
    @staticmethod
    def create_chat(client_socket, database, message):
        pass

        # try:
        #     user = database["users"].find_user(message["data"]["added_user_phone_number"])
        # except:
        #     client_socket.send(
        #         json.dumps(
        #             {"message": "User not found.", "data": None, "status": False}
        #         ).encode("utf-8")
        #     )
        # else:
        #     try:
        #         database["chats"].create_chat(
        #             message["data"]["name"],
        #             "chat",
        #         )
        #     except:
        #         client_socket.send(
        #             json.dumps(
        #                 {
        #                     "message": "Failed while trying to create the chat",
        #                     "data": None,
        #                     "status": False,
        #                 }
        #             ).encode("utf-8")
        #         )
        #     else:
                
        #         try:
        #             chat = database["chats"].find_chat(message["data"]["added_user_phone_number"])
        #         except:
        #             client_socket.send(
        #                 json.dumps(
        #                     {"message": "User not found.", "data": None, "status": False}
        #                 ).encode("utf-8")
        #             )
                # try:
                #     database["users_chats"].create_user_chat(
                #         message["data"]["name"],
                #         message["data"]["phone_number"],
                #         message["data"]["password"],
                #     )
                # except mysql.connector.Error as error:
                #     if error.errno == errorcode.ER_DUP_ENTRY:
                #         client_socket.send(
                #             json.dumps(
                #                 {
                #                     "message": "This user already exists, try another.",
                #                     "data": None,
                #                     "status": False,
                #                 }
                #             ).encode("utf-8")
                #         )
                #         return
                #     else:
                #         client_socket.send(
                #             json.dumps(
                #                 {
                #                     "message": "Error while trying to register, try again or later.",
                #                     "data": None,
                #                     "status": False,
                #                 }
                #             ).encode("utf-8")
                #         )
                #         return
                # else:
                #     client_socket.send(
                #         json.dumps(
                #             {
                #                 "message": "Registered successfully!",
                #                 "data": None,
                #                 "status": True,
                #             }
                #         ).encode("utf-8")
                #     )
                #     return


