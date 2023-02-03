from work_fs import path_near_exefile


def get_urls():
	urls = []
	path_cookies = path_near_exefile("cookies").glob("*")
	for path_cookie in path_cookies:
		urls.append(f"https://www.reddit.com/user/{path_cookie.stem}")

	return urls
