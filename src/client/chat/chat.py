import time
import os
import json
from phonenumbers import parse, NumberParseException


class Chat:
    @staticmethod
    def find_chats_groups(client, user_information, type):
        try:
            client.send(
                json.dumps(
                    {
                        "request_type": "find_chats_groups",
                        "data": {
                            "user_id": user_information["id"],
                            "type": type,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(100000).decode("utf-8"))
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
            results = json.loads(client.recv(100000).decode("utf-8"))
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
            results = json.loads(client.recv(100000).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.2)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

    @staticmethod
    def delete_chat_group(client, id, type):
        print(f"-------- Delete {'Chat' if type == 'chat' else 'Group'} --------\n")
        while True:
            try:
                confirm_deletion = (
                    str(input(f"Do you really want to delete this {'chat' if type == 'chat' else 'group'}? [Y/N]: "))
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
                        "request_type": "delete_chat_group",
                        "data": {
                            "id": id,
                            "type": type,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(100000).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.2)
            os.system("cls" if os.name == "nt" else "clear")
            return results

        else:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

    @staticmethod
    def rename_chat_group(client, id, type):
        print(f"-------- Rename {'Chat' if type == 'chat' else 'Group'} --------\n")
        try:
            new_name = str(input(f"New {'chat' if type == 'chat' else 'group'} name: ")).strip()
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

        client.send(
            json.dumps(
                {
                    "request_type": "rename_chat_group",
                    "data": {
                        "id": id,
                        "type": type,
                        "new_name": new_name,
                    },
                }
            ).encode("utf-8")
        )
        results = json.loads(client.recv(100000).decode("utf-8"))
        print("------------------------------------------------")
        print(results["message"])
        time.sleep(2.2)
        os.system("cls" if os.name == "nt" else "clear")
        return results
    
    @staticmethod
    def group_add_user(client, group_id):
        try:
            print("-------- Add User --------\n => ctrl+c to cancel...")
            while True:
                added_user = str(input("User [Phone Number]: "))
                try:
                    parse(added_user, None)
                    break
                except NumberParseException:
                    print("Invalid Phone Number!")
                    print("------------------------------------------------")
            client.send(
                json.dumps(
                    {
                        "request_type": "group_add_user",
                        "data": {
                            "added_user": added_user,
                            "group_id": group_id,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(100000).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.2)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}
    
    @staticmethod
    def group_remove_user(client, group_id):
        try:
            print("-------- Remove User --------\n => ctrl+c to cancel...")
            client.send(
                json.dumps(
                    {
                        "request_type": "group_add_user",
                        "data": {
                            "group_id": group_id,
                        },
                    }
                ).encode("utf-8")
            )
            results = json.loads(client.recv(100000).decode("utf-8"))
            print("------------------------------------------------")
            print(results["message"])
            time.sleep(2.2)
            os.system("cls" if os.name == "nt" else "clear")
            return results
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}
