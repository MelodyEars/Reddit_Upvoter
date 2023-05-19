import asyncio

from bs4 import BeautifulSoup

from work_fs.async_requests.request import get_html


async def get_username(link: str):
    html_post = await get_html(link)

    soup = BeautifulSoup(html_post, 'html.parser')
    found_elements = soup.find_all('a', class_='author-name whitespace-nowrap text-neutral-content a no-visited no-underline hover:no-underline')

    for element in found_elements:
        return element.text
    else:
        return None


async def get_reveddit_link(link: str):
    username = await get_username(link)
    print(f"username: {username}")
    if username:
        url = f'https://www.reveddit.com/y/{username}/submitted/?showFilters=true&removal_status=not_removed'
        return url
    else:
        return await get_reveddit_link(link)


if __name__ == '__main__':
    asyncio.run(get_reveddit_link('https://www.reddit.com/r/OnlyCurvyGW/comments/13hxdut/does_this_sexy_enough/'))

