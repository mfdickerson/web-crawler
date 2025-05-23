"""
test_web_crawler.py

Unit tests for the WebCrawler class:
- Ensures proper tracking of visited and queued URLs
- Verifies domain filtering and crawl state behavior
"""

import pytest
import pytest_asyncio

from src.web_crawler import WebCrawler

test_data = [
    ("https://www.test-site.com", "https://www.test-site.com"),
    ("test-site.com", "https://test-site.com"),
    ("https://www.test-site.com/", "https://www.test-site.com/"),
    ("https://www.test-site.com/about", "https://www.test-site.com/about"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("url, expected_root_url", test_data)
async def test_initialization(client_session, url, expected_root_url):
    """Tests initialization of WebCrawler class."""
    crawler = WebCrawler(url, client_session)
    assert crawler.root_url == expected_root_url
    assert crawler.site_data == {}
    assert crawler.seen == set()
    assert crawler.visiting == set()
    assert crawler.to_visit == set([expected_root_url])
    assert crawler.max_page_limit == None


@pytest.mark.asyncio
async def test_update_to_visit(client_session):
    """New URLs should be added to to_visit if not already seen."""
    crawler = WebCrawler("https://www.web-crawlers.com", client_session)
    crawler.seen = set(
        [
            "https://www.web-crawlers.com",
            "https://www.web-crawlers.com/peter-parker",
            "https://www.web-crawlers.com/miles-morales",
        ]
    )
    crawler.visiting = set(["https://www.web-crawlers.com/miles-morales"])
    crawler.to_visit = set(["https://www.web-crawlers.com/peni-parker"])

    urls = set(
        [
            "https://www.web-crawlers.com",
            "https://www.web-crawlers.com/peter-parker",
            "https://www.web-crawlers.com/miles-morales",
            "https://www.web-crawlers.com/peni-parker",
            "https://www.web-crawlers.com/miguel-ohara",
        ]
    )

    crawler.update_to_visit(urls)

    assert crawler.to_visit == set(
        ["https://www.web-crawlers.com/peni-parker", "https://www.web-crawlers.com/miguel-ohara"]
    )
