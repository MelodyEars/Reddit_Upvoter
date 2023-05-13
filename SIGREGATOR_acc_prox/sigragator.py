from pathlib import Path

from work_fs import get_list_file

ROOT_DIR = Path(__file__).parent


def get_acc_from_file():
    accounts = []
    proxies = []

    file = 'accounts_proxies.txt'
    file_lins = get_list_file(ROOT_DIR / file)

    for line in file_lins:
        split_line = line.split(" ")
        # accounts.append(split_line[3])
        # proxies.append(split_line[4])
        print(split_line[3])
        # print(split_line[4])
    # return proxies


if __name__ == '__main__':
    get_acc_from_file()

