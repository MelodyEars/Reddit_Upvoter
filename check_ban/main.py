# TODO Choose from list account
# TODO create dict with {account: condition ban}
import asyncio

from check_ban.api_for_check_ban.api import run_browser
# TODO print condition ban == color(grean, red, yellow(shadow ban))

from src import get_urls


def main():
	urls = get_urls()
	dict_acc_cond = asyncio.run(run_browser(urls))


if __name__ == '__main__':
	main()
