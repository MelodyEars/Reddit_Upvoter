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
        url = f'https://www.reveddit.com/y/{username}/submitted/?showFilters=true&removal_status=all'
        # url = f'https://www.reveddit.com/y/{username}/submitted/?showFilters=true&removal_status=not_removed'
        # print(url)
        return url
    else:
        return await get_reveddit_link(link)


if __name__ == '__main__':
    asyncio.run(get_reveddit_link('https://www.reddit.com/r/OnlyCurvyGW/comments/13r4j8h/ever_fucked_a_busty_girl_with_glasses_do_you_want/'))

"""
Hi there, this proxy is not work
Write this Error "No connection could be made because the target machine actively refused it"
192.142.29.69:42548:0Cbln3ryecjTaBW:VQbVBrPsenJD1FF
192.142.29.120:41988:CyaMllM9nLVyxVc:VeOvcH9oqr9GIpu
192.142.29.83:45876:sG4BxXFiKAgASry:CduVyCyq25puEbZ
192.142.29.219:47316:XLIHP3bEbaiqcWi:LG9JrjAt4HSRKiM
192.142.29.153:44656:17OTBFWIGHYPW3r:3mMaBsPRzVO8jnt
192.142.29.67:45978:2GkpEKvHlfYaoJ2:v5eAyaGULYSMAhU
"""



