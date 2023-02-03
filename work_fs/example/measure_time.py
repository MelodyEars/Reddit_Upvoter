import time

def main():
	start = time.time()
	list_accounts = db_get_all_accounts()
	for account in list_accounts:
		print(account.cookie_path.split("/")[1])
	end = time.time()

	elapsed_time = end - start
	print(f"Program execute: {elapsed_time}")

def main2():
	start = time.time()
	path_cookies = path_near_exefile("cookies").glob("*")
	for path_cookie in path_cookies:
		print(path_cookie.stem)
	end = time.time()

	elapsed_time = end - start
	print(f"Program execute: {elapsed_time}")
