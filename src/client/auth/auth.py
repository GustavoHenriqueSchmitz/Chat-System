import os
import time
from phonenumbers import parse, NumberParseException
import json


class Auth:
    @staticmethod
    def login(client):
        while True:
            try:
                print("-------- Login --------\n => ctrl+c to cancel...")
                while True:
                    phone_number = str(input("Phone Number: "))
                    try:
                        parse(phone_number, None)
                        break
                    except NumberParseException:
                        print("Invalid Phone Number")
                password = str(input("Password: "))
                client.send(
                    json.dumps(
                        {
                            "request_type": "login",
                            "data": {
                                "phone_number": phone_number,
                                "password": password,
                            },
                        }
                    ).encode("utf-8")
                )
                results = json.loads(client.recv(1024).decode("utf-8"))
                print("------------------------------------------------")
                print(results["message"])
                time.sleep(3)
                break
            except KeyboardInterrupt:
                break
        os.system("cls" if os.name == "nt" else "clear")
        return results

    @staticmethod
    def sign_up(client):
        while True:
            try:
                print("-------- Sign Up --------\n => ctrl+c to cancel...")
                name = str(input("Name: "))
                while True:
                    phone_number = str(input("Phone Number: "))
                    try:
                        parse(phone_number, None)
                        break
                    except NumberParseException:
                        print("Invalid Phone Number")
                password = str(input("Password: "))
                client.send(
                    json.dumps(
                        {
                            "request_type": "sign_up",
                            "data": {
                                "name": name,
                                "phone_number": phone_number,
                                "password": password,
                            },
                        }
                    ).encode("utf-8")
                )
                results = json.loads(client.recv(1024).decode("utf-8"))
                print("------------------------------------------------")
                print(results["message"])
                time.sleep(3)
                break
            except KeyboardInterrupt:
                break
        os.system("cls" if os.name == "nt" else "clear")
        return results["error"]
