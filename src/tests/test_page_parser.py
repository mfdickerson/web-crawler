"""
test_page_parser.py

Unit tests for the PageParser class, including:
- URL repair and normalization
- Absolute URL resolution
- Subdomain filtering
- Page content parsing logic
"""

from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import urlparse

import pytest
import pytest_asyncio

from src.web_crawler import PageParser

# Test Bad HTML
ugly_page = """
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Web Crawlers</title></head>
<body>
<h1>
   Famous Web Crawlers
</h1><p><a href="https://www.web-crawlers.com/peter-parker">Peter Parker</a></p>
<p><a href="https://www.web-crawlers.com/shelob">Shelob</a></p></body>
</html>
"""
# Test Good HTLM
beautiful_page = """<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <title>
   Web Crawlers
  </title>
 </head>
 <body>
  <h1>
   Famous Web Crawlers
  </h1>
  <p>
   <a href="https://www.web-crawlers.com/peter-parker">
    Peter Parker
   </a>
  </p>
  <p>
   <a href="https://www.web-crawlers.com/shelob">
    Shelob
   </a>
  </p>
 </body>
</html>
"""


@pytest.fixture
def mock_aiohttp_get():
    """Mocked aiohttp.ClientSession.get method returning a fixed HTML page."""
    mock_response = MagicMock()
    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = None
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value=ugly_page)

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        yield mock_response


def test_page_parser_init():
    """Test direct initialization of PageParser with raw HTML."""
    page_parser = PageParser("https://www.web-crawlers.com", ugly_page)

    assert page_parser.page_url == "https://www.web-crawlers.com"
    assert page_parser.beautiful_page.prettify() == beautiful_page


@pytest.mark.asyncio
async def test_load_page(client_session, mock_aiohttp_get):
    """Test async loading of a PageParser instance via PageParser.load_page()."""
    page_parser = await PageParser.load_page(client_session, "https://www.web-crawlers.com")

    assert page_parser.page_url == "https://www.web-crawlers.com"
    assert page_parser.beautiful_page.prettify() == beautiful_page


# TO DO: Test exponential backoff in PageParser.load_page()


def test_get_links():
    """ "Test that get_links returns a correct set of hrefs."""
    page_parser = PageParser("https://www.web-crawlers.com", ugly_page)
    links = page_parser.get_links()
    assert links == set(
        ["https://www.web-crawlers.com/peter-parker", "https://www.web-crawlers.com/shelob"]
    )


test_data = [
    ("https://web-crawlers.com", "https://web-crawlers.com"),
    ("web-crawlers.com", "https://web-crawlers.com"),
    ("web-crawlers.com/peter-parker", "https://web-crawlers.com/peter-parker"),
]


@pytest.mark.parametrize("url, expected_url", test_data)
def test_repair_incomplete_url(url, expected_url):
    """Ensure repair_incomplete_url adds missing scheme as necessary."""
    repaired_url = PageParser.repair_incomplete_url(url)

    assert repaired_url == expected_url


test_data = [
    ("https://www.web-crawlers.com/peter-parker", "https://www.web-crawlers.com/peter-parker"),
    ("/miles-morales", "https://www.web-crawlers.com/miles-morales"),
    ("/gwen-stacy/", "https://www.web-crawlers.com/gwen-stacy/"),
]


@pytest.mark.parametrize("href, expected_absolute_url", test_data)
def test_get_absolute_url_from_href(href, expected_absolute_url):
    """Validate conversion of relative href to absolute URL."""
    page_parser = PageParser("https://www.web-crawlers.com", ugly_page)

    absolute_url = page_parser.get_absolute_url_from_href(href)

    assert absolute_url == expected_absolute_url


test_data = [
    (
        "https://www.web-crawlers.com",
        set(["https://www.web-crawlers.com/peter-parker", "https://www.spider-man.com"]),
        set(["https://www.web-crawlers.com/peter-parker"]),
    ),
    (
        "www.web-crawlers.com",
        set(["https://www.web-crawlers.com/peter-parker", "https://www.spider-man.com"]),
        set(["https://www.web-crawlers.com/peter-parker"]),
    ),
    pytest.param(
        "web-crawlers.com",
        set(["https://www.web-crawlers.com/peter-parker", "https://www.spider-man.com"]),
        set(["https://www.web-crawlers.com/peter-parker"]),
        marks=pytest.mark.skip(
            reason="Need to determine desired behavior for incomplete URLs"
        ),  # TODO
    ),
]


@pytest.mark.parametrize("page_url, links, expected_subdomains", test_data)
def test_get_subdomains(page_url, links, expected_subdomains):
    """Check that only links from the same domain are returned."""
    page_parser = PageParser(page_url, None)
    subdomains = page_parser.get_subdomains(links)
    print(f"Self netloc: {urlparse(page_parser.page_url).netloc}")
    print(f"Self path: {urlparse(page_parser.page_url).path}")

    print("Link:")
    for link in links:
        print(urlparse(link).netloc)

    assert subdomains == expected_subdomains
