import asyncio
from playwright.async_api import async_playwright


async def get_detail(context, url):
	page = await context.new_page()
	await page.goto(url)
	await page.wait_for_load_state(state="networkidle")
	await page.wait_for_timeout(1000)
	await page.close
	# TODO return response ban, shadow ban, None


async def open_new_pages(context, urls):
	async with asyncio.TaskGroup() as tg:
		for url in urls:
			task = tg.create_task(
				get_detail(context, url)
			)

	# TODO return dict{url: response}


async def run_browser(urls):
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=False)
		context = await browser.new_context()
		await open_new_pages(context, urls)

	# TODO return func
