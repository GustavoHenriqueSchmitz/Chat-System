import os
import time
from phonenumbers import parse, NumberParseException
import json


class User:
    @staticmethod
    def change_name(client, user_information):
        try:
            print("-------- Change Name --------\n => ctrl+c to cancel...")
            new_name = str(input("New name: ")).strip()
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

        client.send(
            json.dumps(
                {
                    "request_type": "change_user_name",
                    "data": {
                        "new_name": new_name,
                        "phone_number": user_information["phone_number"],
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

    @staticmethod
    def change_phone_number(client, user_information):
        try:
            print("-------- Change Number --------\n => ctrl+c to cancel...")
            new_phone_number = str(input("New phone number: ")).strip()
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}

        client.send(
            json.dumps(
                {
                    "request_type": "change_user_phone_number",
                    "data": {
                        "new_phone_number": new_phone_number,
                        "phone_number": user_information["phone_number"],
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

    @staticmethod
    def change_password(client, user_information):
        print("-------- Change Password --------\n => ctrl+c to cancel...")
        try:
            new_password = str(input("New Password: "))
        except KeyboardInterrupt:
            os.system("cls" if os.name == "nt" else "clear")
            return {"message": None, "data": None, "status": False}
        while True:
            try:
                new_password_confirmation = str(input("Confirm you new password: "))
                if new_password == new_password_confirmation:
                    client.send(
                        json.dumps(
                            {
                                "request_type": "change_user_password",
                                "data": {
                                    "new_password": new_password,
                                    "phone_number": user_information["phone_number"],
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
                    print("Mismatched password confirmation.")
                    print("------------------------------------------------")
                    continue

            except KeyboardInterrupt:
                os.system("cls" if os.name == "nt" else "clear")
                return {"message": None, "data": None, "status": False}

    @staticmethod
    def delete_user(client, user_information):
        print("-------- Delete User --------\n")
        while True:
            try:
                confirm_deletion = (
                    str(input("Do you really want to delete your user? [Y/N]: "))
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
                        "request_type": "delete_user",
                        "data": user_information["phone_number"],
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
