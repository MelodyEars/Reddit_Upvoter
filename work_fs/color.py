from colorama import Fore, Style, Back


def warning_text(text):
    print(Fore.RED + "warning! -> " + Style.RESET_ALL + Back.RED + Fore.WHITE + str(text) + Style.RESET_ALL)


def blue_color(text):
    return Fore.LIGHTBLUE_EX + str(text) + Style.RESET_ALL


def green_color(text):
    return Fore.GREEN + str(text) + Style.RESET_ALL


def light_green_color(text):
    return Fore.LIGHTGREEN_EX + str(text) + Style.RESET_ALL


def cyan_color(text):
    return Fore.LIGHTCYAN_EX + str(text) + Style.RESET_ALL


def yellow_color(text):
    return Fore.YELLOW + str(text) + Style.RESET_ALL


def magenta_color(text):
    return Fore.LIGHTMAGENTA_EX + str(text) + Style.RESET_ALL
