"""
test_web_crawler.py

Integration Test for the WebCrawler.
"""

import aiohttp
import pytest
import pytest_asyncio

from src.web_crawler import WebCrawler


@pytest.fixture
def test_url():
    return "https://www.overstory.com"


@pytest_asyncio.fixture()
async def client_session():
    async with aiohttp.ClientSession(trust_env=True) as client_session:
        return client_session


@pytest.mark.asyncio
async def test_web_crawler(client_session, test_url):
    """Tests full functionality of WebCrawler class."""
    root_url = test_url
    max_page_limit = 5

    async with aiohttp.ClientSession(trust_env=True) as client_session:
        web_crawler = WebCrawler(root_url, client_session)
        web_crawler.max_page_limit = max_page_limit

        await web_crawler.crawl()

    assert web_crawler.root_url == test_url
    assert web_crawler.max_page_limit == max_page_limit
    assert len(web_crawler.site_data) == max_page_limit
    assert len(web_crawler.seen) == max_page_limit
    assert web_crawler.visiting == set()
