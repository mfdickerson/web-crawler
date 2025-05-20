import pytest
from src import web_crawler
import pytest_asyncio

@pytest.fixture
def test_url():
    return 'https://www.overstory.com'


@pytest.mark.asyncio
async def test_get_page(event_loop, test_url):
    import aiohttp
    async with aiohttp.ClientSession(loop=event_loop) as client_session:
        # initialize the objects
        crawler = web_crawler.WebCrawler(test_url, client_session)
        response = await crawler.get_page(test_url)
    print(response)