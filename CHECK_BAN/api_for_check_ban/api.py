# import asyncio
# from pathlib import Path
#
# from playwright.async_api import async_playwright, Browser
# from playwright_stealth import stealth_async
#
# DICT_ACC_BAN = {}
# # EXECUTABLE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
# EXECUTABLE_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
#
#
# async def check_and_add_ban(page, path_cookie: Path):
# 	# permanent ban
# 	if await (page.get_by_role("heading", name="This account has been suspended .").is_visible(timeout=3000)):
# 		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = "permanent"
#
# 	# shadow ban
# 	elif await page.get_by_role(
# 			"heading", name="Sorry, nobody on Reddit goes by that name.", exact=True).is_visible(timeout=3000):
# 		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = "shadow"
#
# 	# without ban
# 	else:
# 		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = None
#
#
# async def open_page(browser, path_cookie: Path):
# 	page = await browser.new_page()
# 	await stealth_async(page)
# 		# domcontentloaded
# 	url = f"https://www.reddit.com/user/{path_cookie.stem}"
# 	await page.goto(url, wait_until="networkidle")
# 	# networkidle
# 	if await page.locator('xpath=//button[contains(text(), "Accept all")]').is_visible():
# 		await page.locator('xpath=//button[contains(text(), "Accept all")]').click()
# 		await page.wait_for_load_state("networkidle")
#
# 	await check_and_add_ban(page, path_cookie)
#
# 	await page.close()
#
#
# async def run_page(browser, path_cookies):
# 	print("Працюю...")
# 	tasks = [asyncio.create_task(open_page(browser, path_cookie)) for path_cookie in path_cookies]
# 	await asyncio.gather(*tasks)
# 	print("Закінчив працювати.")


# async def run_session(path_cookies: list, count_page: int):
# 	async with async_playwright() as playwright:
# 		browser = await playwright.chromium.launch(headless=False, executable_path=EXECUTABLE_PATH)
#
# 		num = count_page
# 		next_paths = path_cookies[:num]
#
# 		while next_paths:
# 			# context = await browser.new_context()
# 			await run_page(browser, next_paths)
# 			resent_num = num
# 			num += count_page
# 			next_paths = path_cookies[resent_num:num]
# 			# await context.close()
#
# 		await browser.close()


import asyncio
from pathlib import Path

import aiohttp
from fake_useragent import UserAgent
from loguru import logger

from work_fs.PATH import auto_create, path_near_exefile
from work_fs.write_to_file import write_line
from work_fs.read_file import get_str_file


COUNT = 1
DICT_ACC_BAN = {}


def unpack_ban(html):
	permanent = 'suspended' in html
	if permanent:
		return "permanent"

	shadow = 'Sorry, nobody on Reddit goes by that name.' in html
	if shadow:
		return "shadow"

	return None


def del_all_responses():
	folder_with_resps = path_near_exefile("responses")
	for file in folder_with_resps.iterdir():
		file.unlink()


async def fetch(session, url):
	global COUNT

	async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
		html_to_file = await response.text()
		filepath: Path = auto_create(path_near_exefile("responses"), _type="dir") / f"output{COUNT}.html"
		write_line(filepath, html_to_file)
		html = get_str_file(filepath)

		COUNT += 1

		if not ('page not found' in html and html is None):
			return html

		logger.error(f"page not found: {url}")
		await asyncio.sleep(2)

		return await fetch(session, url)


async def get_ban(path_cookie: Path):
	url = f"https://www.reddit.com/user/{path_cookie.stem}"

	async with aiohttp.ClientSession() as session:
		html = await fetch(session, url)
		ban = unpack_ban(html)

		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = ban

		print(f"{url}: {ban}")


async def create_task(path_cookies: list):
	tasks = [asyncio.create_task(get_ban(path_cookie)) for path_cookie in path_cookies]
	await asyncio.gather(*tasks)


def check_ban(path_cookies: list[Path]):
	asyncio.run(create_task(path_cookies))
	del_all_responses()

	return DICT_ACC_BAN
