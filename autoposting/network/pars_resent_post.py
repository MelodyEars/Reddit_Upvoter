import asyncio
from pathlib import Path

import aiohttp
from fake_useragent import UserAgent
from loguru import logger


from work_fs.PATH import auto_create, path_near_exefile, delete_dir
from work_fs.write_to_file import write_line
from work_fs.read_file import get_str_file


def del_all_responses():
	folder_with_resps = path_near_exefile("responses")
	delete_dir(folder_with_resps)


async def fetch(session, url):

	async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
		html_to_file = await response.text()
		filepath: Path = auto_create(path_near_exefile("responses"), _type="dir") / f"output{COUNT}.html"
		write_line(filepath, html_to_file)
		html = get_str_file(filepath)

		if not ('page not found' in html and html is None):
			return html

		logger.error(f"page not found: {url}")
		await asyncio.sleep(2)

		return await fetch(session, url)


async def get_ban(path_cookie: Path):
	url = f"https://www.reddit.com/user/{path_cookie.stem}"

	async with aiohttp.ClientSession() as session:
		html = await fetch(session, url)


async def create_task(path_cookies: list):
	tasks = [asyncio.create_task(get_ban(path_cookie)) for path_cookie in path_cookies]
	await asyncio.gather(*tasks)


def check_ban(path_cookies: list[Path]):
	asyncio.run(create_task(path_cookies))
	del_all_responses()
