import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, BrowserContext, Browser
from playwright_stealth import stealth_async


LIST_ACC_BAN = []


async def check_and_add_ban(page, path_cookie: Path):

	if await page.get_by_role("img", name="User Avatar").is_visible(timeout=10000):
		return
	else:
		LIST_ACC_BAN.append(f'cookies/{path_cookie.name}')


async def open_page(browser: Browser, path_cookie: Path):
	context = await browser.new_context()
	page = await context.new_page()
	await stealth_async(page)

	url = f"https://www.reddit.com/user/{path_cookie.stem}"
	await page.goto(url, wait_until="networkidle", timeout=0)

	if await page.locator('xpath=//button[contains(text(), "Accept all")]').is_visible(timeout=10000):
		await page.locator('xpath=//button[contains(text(), "Accept all")]').click()
		await page.wait_for_load_state("networkidle")
		await check_and_add_ban(page, path_cookie)

	else:
		await check_and_add_ban(page, path_cookie)

	await page.close()


async def run_browser(path_cookies):
	async with async_playwright() as playwright:
		browser = await playwright.chromium.launch(headless=False, executable_path=r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe')
		print("Працюю...")
		await asyncio.wait(
			[asyncio.create_task(open_page(browser, path_cookie)) for path_cookie in path_cookies],
			return_when=asyncio.ALL_COMPLETED,
		)

		await browser.close()
		print("Закінчив працювати.")


def check_ban(path_cookies: str, count_page: int):
	num = count_page
	next_paths = path_cookies[:num]

	while next_paths:
		asyncio.run(run_browser(next_paths))

		resent_num = num
		num += count_page
		next_paths = path_cookies[resent_num:num]

	return LIST_ACC_BAN


