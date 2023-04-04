import requests
import os


URL_BASE = "http://146.19.247.196"
token = str


def get_token_from_file() -> token:
    with open("TOKEN.txt", encoding="utf-8") as file:
        return file.read()


def get_or_create_token() -> token:
    if os.path.exists("TOKEN.txt"):
        return get_token_from_file()
    else:
        token = input("Введите ваш токен телеграм бота.\n")
        with open("TOKEN.txt", "w", encoding="utf-8") as file:
            file.write(token)
        return token


def check_access() -> bool:
    token = get_or_create_token()
    proj = "proj1"
    port = ":8000/"

    data = {'token_bot': token, 'project_name': proj}

    full_url = URL_BASE + port + "ask_access/"
    resp = requests.post(full_url, json=data)
    if resp.json()['status'] == "ok":
        return True
    else:
        return False


if __name__ == '__main__':
    has_access = check_access()


