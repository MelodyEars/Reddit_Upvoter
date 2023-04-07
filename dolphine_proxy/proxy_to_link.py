from pathlib import Path

from work_fs import get_list_file


def get_proxy():
    path_to_file = Path(__file__).parent / "proxies.txt"
    list_proxy_from_file = get_list_file(path_to_file)
    for proxy in list_proxy_from_file:
        old_proxy = proxy.split(":")
        '74.50.9.2:45687:rjHUS9gBR3AQV5b:c2EjPzTD8ejGSuq'
        new_proxy = f'http://{old_proxy[2]}:{old_proxy[3]}@{old_proxy[0]}:{old_proxy[1]}'
        print(new_proxy)


if __name__ == '__main__':
    get_proxy()

