import time
import os
import json
from phonenumbers import parse, NumberParseException


class Chat:
    @staticmethod
    def find_chats(client, user_information, chat_type):
        try:
            client.send(
                json.dumps(
                    {
                        "request_type": "find_chats",
                        "data": {
                            "user_id": user_information["id"],
                            "chat_type": chat_type,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(1024).decode("utf-8"))
            if results["status"] == False:
                print("------------------------------------------------")
                print(results["message"])
                time.sleep(2.5)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

    @staticmethod
    def create_chat(client, user_information):
        try:
            print("-------- Create Chat --------\n => ctrl+c to cancel...")
            while True:
                chat_user = str(input("Add User [Phone Number]: ")).strip()
                try:
                    parse(chat_user, None)
                    break
                except NumberParseException:
                    print("Invalid Phone Number")
                    print("------------------------------------------------")
                    continue
            chat_name = str(input("Chat Name: ")).strip()

            client.send(
                json.dumps(
                    {
                        "request_type": "create_chat",
                        "data": {
                            "user_id": user_information["id"],
                            "added_user_phone_number": chat_user,
                            "chat_name": chat_name,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(1024).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.5)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

    @staticmethod
    def create_group(client, user_information):
        try:
            print("-------- Create Group --------\n => ctrl+c to cancel...")
            group_users = [user_information["phone_number"]]
            while True:
                print("-------- Digit exit for finish --------")
                group_user = str(input("Add User [Phone Number]: ")).strip()
                if group_user.lower() == "exit":
                    break
                elif group_user in group_users:
                    print("------------------------------------------------")
                    print("This user was already added!")
                    continue

                try:
                    parse(group_user, None)
                    group_users.append(group_user)
                except NumberParseException:
                    print("Invalid Phone Number")
                    print("------------------------------------------------")
            group_name = str(input("Group Name: ")).strip()

            client.send(
                json.dumps(
                    {
                        "request_type": "create_group",
                        "data": {
                            "user_id": user_information["id"],
                            "added_users_phone_number": group_users,
                            "group_name": group_name,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(1024).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.5)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}
