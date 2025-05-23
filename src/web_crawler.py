"""
web_crawler.py

Asynchronous command-line web crawler.

This module defines a simple crawler that:
- Begins at a user-defined root URL
- Traverses internal links on the same domain
- Limits crawling optionally by page count
- Outputs all visited URLs and their discovered links

Uses aiohttp for HTTP requests and BeautifulSoup for HTML parsing.

Usage:
    python web_crawler https://example.com [--max_page_limit=3]

Author: Mark Dickerson
"""

import argparse
import asyncio
import logging
import random
from urllib.parse import urljoin, urlparse, urlunparse

import aiohttp

# import async_timeout
from bs4 import BeautifulSoup

logger = logging.getLogger()

# A list of user-agent strings to randomize requests and avoid simple bot detection
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
]


class PageParser:
    """Parses a webpage to extract links and normalize URLs."""

    max_attempts = 3  # TODO: Make this customizable by user
    max_timeout = 10

    def __init__(self, page_url, page):
        self.page_url = PageParser.repair_incomplete_url(page_url)
        if page:
            self.beautiful_page = BeautifulSoup(page, "html.parser")
        else:
            self.beautiful_page = None

    @classmethod
    async def load_page(cls, session, page_url):
        """Fetches and returns a parsed PageParser instance for the given URL.

        Args:
            session (aiohttp.ClientSession): The HTTP session used for requests.
            page_url (str): The URL to fetch.

        Returns:
            PageParser: PageParser object with extracted data.
        """
        headers = {"User-Agent": user_agent_list[random.randint(0, len(user_agent_list) - 1)]}
        for attempt in range(cls.max_attempts):
            try:
                timeout = aiohttp.ClientTimeout(total=cls.max_timeout)
                async with session.get(page_url, headers=headers, timeout=timeout) as response:
                    if response.status == 200:
                        page = await response.text()
                        return cls(page_url, page)  # Exit the loop if successful
                    else:
                        print(page_url, response.status)
                    return cls(page_url, None)
            except aiohttp.ClientError as e:  # TODO: Other errors that may require backoff?
                if attempt < (cls.max_attempts - 1):
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {page_url} after {cls.max_attempts}: {e}")
                    raise  # Re-raise error after max_attempts reached

    def get_links(self) -> set[str]:
        """Extracts all anchor tag href links as absolute URLs.

        Returns:
            set[str]: Absolute URLs found in anchor tags.
        """
        links = self.beautiful_page.select("a[href]")
        return_urls = set()
        for link in links:
            return_urls.add(self.get_absolute_url_from_href(link["href"]))

        return return_urls

    def get_absolute_url_from_href(self, href) -> str:
        """Converts a relative URL to an absolute one as needed.

        Args:
            href (str): The href string from an anchor tag.

        Returns:
            str: Absolute URL.
        """
        parsed_reference = urlparse(href)
        if parsed_reference.scheme != "http":
            absolute_url = urljoin(self.page_url, href)
        else:
            absolute_url = href

        return absolute_url

    def get_subdomains(self, links) -> set[str]:
        """Filters links to only those that match the domain of the root URL.

        Args:
            links (set[str]): A set of absolute URLs.

        Returns:
            set[str]: Filtered URLs that match the domain of the root URL.
        """
        return_urls = set()
        for link in links:
            # ensure the crawled link belongs to the target domain
            if urlparse(link).netloc == urlparse(self.page_url).netloc:
                return_urls.add(link)

        return return_urls

    # TODO: async def reload_page(session)

    @classmethod
    def repair_incomplete_url(cls, url) -> str:
        """Ensures a URL has a scheme and correct format.

        Args:
            url (str): A potentially incomplete URL.

        Returns:
            str: Properly formatted URL with scheme and netloc.
        """
        scheme, netloc, path, params, query, fragment = urlparse(url)

        if scheme == "":
            scheme = "https"
        if not netloc:
            netloc, path = path, ""

        updated_url = urlunparse((scheme, netloc, path, params, query, fragment))
        return updated_url


class WebCrawler:
    """Asynchronous web crawler for a single domain.

    Given a starting URL, the crawler visits each URL it finds on the same domain.
    It saves each URL visited, and a list of links found on that page.
    The crawler is limited to one subdomain.
    """

    def __init__(self, root_url, session):
        self.session = session
        self.root_url = PageParser.repair_incomplete_url(
            root_url
        )  # TODO: Additional URL validation

        self.site_data = {}
        self.seen = set()  # "Visited" and "Visiting" pages
        self.visiting = set()
        # A set() is chosen for the to_visit queue to ensure a non-deterministic crawl order.
        # Using a psuedo-random crawl will ensure efficient traversal of adversarial page structures
        # that FIFO and FILO queues may struggle with.
        self.to_visit = set([self.root_url])
        self.max_page_limit = None  # Set manually with web_crawler.max_page_limit = 100

    def print_site_data(self):
        """Prints all visited URLs and the links found on each page."""
        for key, value in self.site_data.items():
            print(f"{key}")
            for link in value:
                print(f"  - {link}")
            print("\n")

    async def process_page(self, url):
        """Processes a single page: fetches, extracts links, updates crawl state.

        Args:
            url (str): URL of the page to process.
        """
        logger.info(f"Begin processing: {url}")

        try:
            page_parser = await PageParser.load_page(self.session, url)
            if page_parser.beautiful_page is not None:
                logger.info(f"Retrieving links from: {url}")
                links = page_parser.get_links()
                logger.info(f"Saving links from: {url}")
                self.site_data.update({url: links})

                logger.info(f"Updating queue...")
                new_urls = page_parser.get_subdomains(links)
                self.update_to_visit(new_urls)
        except aiohttp.ClientConnectorError as e:
            logger.error("Connection Error", str(e))
        except aiohttp.InvalidUrlClientError as e:
            logger.error(f"Invalid URL: {url}", str(e))

        self.visiting.remove(url)
        logger.info(f"End processing:   {url}")

    async def crawl(self):
        """Main crawling loop, runs until the queue is exhausted or limit is reached."""
        if self.max_page_limit is None:
            logger.warning("No max_page_limit set")

        logger.info("Beginning Crawl")

        tasks = []
        task_counter = 0

        try:
            while (len(self.to_visit) > 0 or len(self.visiting) > 0) and (
                self.max_page_limit is None or task_counter < self.max_page_limit
            ):
                if len(self.to_visit) > 0:
                    next_url = self.to_visit.pop()
                    self.visiting.add(next_url)
                    self.seen.add(next_url)

                    tasks.append(asyncio.create_task(self.process_page(next_url)))
                    task_counter += 1
                else:
                    await asyncio.sleep(0)  # Allow other tasks to run

            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.warning("Crawling cancelled. Cancelling remaining tasks...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during crawl: {e}")
        finally:
            logger.info(f"{len(self.site_data)} pages crawled")

    def update_to_visit(self, urls):
        """Adds new URLs to the queue if not already visited or in progress.

        Args:
            urls (set[str]): Set of URLs to consider for crawling.
        """
        for url in urls:
            if url not in self.seen:  # Not visited and not visiting
                self.to_visit.add(url)
                logger.info(f"Adding URL to queue: {url}")


async def main():
    """Parses arguments, creates crawler, and starts the crawl."""

    try:
        parser = argparse.ArgumentParser(description="Web Crawler")
        parser.add_argument("starting_url", help="Starting URL")
        parser.add_argument("--max_page_limit", help="Max Page Limit", type=int, required=False)
        args = parser.parse_args()

        root_url = args.starting_url
        max_page_limit = args.max_page_limit

        async with aiohttp.ClientSession(trust_env=True) as client_session:
            # root_url = input("Enter a valid URL: ")
            web_crawler = WebCrawler(root_url, client_session)
            if max_page_limit:
                web_crawler.max_page_limit = max_page_limit

            await web_crawler.crawl()

        web_crawler.print_site_data()
    except KeyboardInterrupt:
        logger.warning("Web Crawler interrupted by user.")


if __name__ == "__main__":
    asyncio.run(main())
