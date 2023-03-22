import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, Browser
from playwright_stealth import stealth_async

DICT_ACC_BAN = {}
# EXECUTABLE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
EXECUTABLE_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'


async def check_and_add_ban(page, path_cookie: Path):
	# permanent ban
	if await (page.get_by_role("heading", name="This account has been suspended .").is_visible(timeout=3000)):
		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = "permanent"

	# shadow ban
	elif await page.get_by_role(
			"heading", name="Sorry, nobody on Reddit goes by that name.", exact=True).is_visible(timeout=3000):
		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = "shadow"

	# without ban
	else:
		DICT_ACC_BAN[f"cookies/{path_cookie.name}"] = None


async def open_page(browser, path_cookie: Path):
	page = await browser.new_page()
	await stealth_async(page)
		# domcontentloaded
	url = f"https://www.reddit.com/user/{path_cookie.stem}"
	await page.goto(url, wait_until="networkidle")
	# networkidle
	if await page.locator('xpath=//button[contains(text(), "Accept all")]').is_visible():
		await page.locator('xpath=//button[contains(text(), "Accept all")]').click()
		await page.wait_for_load_state("networkidle")

	await check_and_add_ban(page, path_cookie)

	await page.close()


async def run_page(browser, path_cookies):
	print("Працюю...")
	# await asyncio.wait(
	# 	[asyncio.create_task(open_page(context, path_cookie)) for path_cookie in path_cookies],
	# 	return_when=asyncio.ALL_COMPLETED,
	# )
	tasks = [asyncio.create_task(open_page(browser, path_cookie)) for path_cookie in path_cookies]
	await asyncio.gather(*tasks)
	print("Закінчив працювати.")


async def run_session(path_cookies: list, count_page: int):
	async with async_playwright() as playwright:
		browser = await playwright.chromium.launch(headless=False, executable_path=EXECUTABLE_PATH)

		num = count_page
		next_paths = path_cookies[:num]

		while next_paths:
			# context = await browser.new_context()
			await run_page(browser, next_paths)
			resent_num = num
			num += count_page
			next_paths = path_cookies[resent_num:num]
			# await context.close()

		await browser.close()


def check_ban(path_cookies: list, count_page: int):
	asyncio.run(run_browser(path_cookies, count_page))

	return DICT_ACC_BAN