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
                time.sleep(2.2)
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
            time.sleep(2.2)
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
            time.sleep(2.2)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

    @staticmethod
    def delete_chat(client, chat_id, chat_type):
        print("-------- Delete Chat --------\n")
        while True:
            try:
                confirm_deletion = (
                    str(input("Do you really want to delete this chat? [Y/N]: "))
                    .strip()
                    .lower()
                )
                if confirm_deletion != "y" and confirm_deletion != "n":
                    print("Invalid option, digit [Y/N]")
                    print("------------------------------------------------")
                    time.sleep(2)
                    continue
                else:
                    break
            except KeyboardInterrupt:
                os.system("cls" if os.name == "nt" else "clear")
                return {"message": None, "data": None, "status": False}

        if confirm_deletion == "y":
            client.send(
                json.dumps(
                    {
                        "request_type": "delete_chat",
                        "data": {
                            "chat_id": chat_id,
                            "chat_type": chat_type,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(1024).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.2)
            os.system("cls" if os.name == "nt" else "clear")
            return results

        else:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

    @staticmethod
    def rename_chat(client, chat_id, chat_type):
        print("-------- Rename Chat --------\n")
        try:
            new_chat_name = str(input("New chat name: ")).strip()
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

        client.send(
            json.dumps(
                {
                    "request_type": "rename_chat",
                    "data": {
                        "chat_id": chat_id,
                        "chat_type": chat_type,
                        "new_chat_name": new_chat_name,
                    },
                }
            ).encode("utf-8")
        )
        results = json.loads(client.recv(1024).decode("utf-8"))
        print("------------------------------------------------")
        print(results["message"])
        time.sleep(2.2)
        os.system("cls" if os.name == "nt" else "clear")
        return results
