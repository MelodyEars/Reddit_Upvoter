import os


def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')
