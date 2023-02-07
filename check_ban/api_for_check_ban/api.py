import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, BrowserContext
from playwright_stealth import stealth_async


LIST_ACC_COND = []


async def check_and_add_ban(page, path_cookie):
	if await page.get_by_role("img", name="User Avatar").is_visible(timeout=1000):
		LIST_ACC_COND.append((path_cookie, False))
	else:
		LIST_ACC_COND.append((path_cookie, True))


async def open_page(context: BrowserContext, path_cookie: Path):
	page = await context.new_page()
	await stealth_async(page)

	url = f"https://www.reddit.com/user/{path_cookie.stem}"
	await page.goto(url, wait_until="domcontentloaded", timeout=0)

	if await page.locator('xpath=//button[contains(text(), "Accept all")]').is_visible(timeout=10000):
		await page.locator('xpath=//button[contains(text(), "Accept all")]').click()
		await check_and_add_ban(page, path_cookie)
	else:
		await check_and_add_ban(page, path_cookie)

	await page.close()


async def run_browser(path_cookies):
	async with async_playwright() as playwright:
		browser = await playwright.chromium.launch(headless=False, channel="chrome")
		context = await browser.new_context()

		await asyncio.wait(
			[asyncio.create_task(open_page(context, path_cookie)) for path_cookie in path_cookies],
			return_when=asyncio.ALL_COMPLETED,
		)
		await context.close()
		await browser.close()


def check_ban(path_cookies, count_page: int):
	path_cookies = list(path_cookies)
	num = count_page
	next_paths = path_cookies[:num]

	while next_paths:
		asyncio.run(run_browser(next_paths))

		resent_num = num
		num += count_page
		next_paths = path_cookies[resent_num:num]

	return LIST_ACC_COND
