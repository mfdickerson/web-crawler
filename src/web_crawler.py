import argparse
import aiohttp
import asyncio
# import async_timeout
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
import random

import logging

logger = logging.getLogger()

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

class PageParser:
    def __init__(self, page_url, page):
        self.page_url = PageParser.repair_incomplete_url(page_url)
        if page:
            self.beautiful_page = BeautifulSoup(page, "html.parser")
        else:
            self.beautiful_page = None

    @classmethod
    async def load_page(cls, session, page_url):
        # with async_timeout.timeout(10):
        headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]}
        async with session.get(page_url, headers=headers) as response:
            if response.status == 200:
                page = await response.text()
                return cls(page_url, page)
            else:
                print(page_url, response.status)
            return cls(page_url, None)
            
    def get_links(self):
        links = self.beautiful_page.select("a[href]")
        return_urls = set()
        for link in links:
            return_urls.add(self.get_absolute_url_from_href(link["href"]))

        return return_urls
    
    def get_absolute_url_from_href(self, href):
        parsed_reference = urlparse(href)
        if parsed_reference.scheme != "http":
            absolute_url = urljoin(self.page_url, href)
        else:
            absolute_url = href

        return absolute_url

    def get_subdomains(self, links):
        return_urls = set()
        for link in links:
            # ensure the crawled link belongs to the target domain
            if urlparse(link).netloc == urlparse(self.page_url).netloc:
                return_urls.add(link)

        return return_urls
    
    # TODO: async def reload_page(session)

    @classmethod
    def repair_incomplete_url(cls, url):
        scheme, netloc, path, params, query, fragment = urlparse(url)

        if scheme == '':
            scheme = 'https'
        if not netloc:
            netloc, path = path, ''

        updated_url = urlunparse((scheme, netloc, path, params, query, fragment))
        return updated_url





class WebCrawler:

    def __init__(self, root_url, session):
        self.session = session
        self.root_url = PageParser.repair_incomplete_url(root_url) # TODO: Additional URL validation

        self.site_data = {}
        self.visited = set()
        self.visiting = set()
        self.to_visit = set([self.root_url])
        self.max_page_limit = None # Set manually with web_crawler.max_page_limit = 100


    def print_site_data(self):
        for key, value in self.site_data.items():
            print(f"{key}")
            for link in value:
                print(f"  - {link}")
            print("\n")

        
    async def process_page(self, url):
        logger.info(f"Begin processing: {url}")

        try:
            page_parser = await PageParser.load_page(self.session, url)
            if page_parser.beautiful_page is not None:
                logger.info(f"Retrieving links from: {url}")
                links = page_parser.get_links()
                self.site_data.update({url: links})

                logger.info(f"Updating queue")
                new_urls = page_parser.get_subdomains(links)
                self.update_to_visit(new_urls)
        except aiohttp.ClientConnectorError as e:
            logger.error('Connection Error', str(e))
        except aiohttp.InvalidUrlClientError as e:
            logger.error('Invalid URL', str(e))

        self.visiting.remove(url)
        self.visited.add(url)
        logger.info(f"End processing:   {url}")


    async def crawl(self):
        if self.max_page_limit is None:
            logger.warning("No max_page_limit set")

        logger.info("Beginning Crawl")

        tasks = []
        task_counter = 0
        while (len(self.to_visit) > 0 or len(self.visiting) > 0) and (self.max_page_limit is None or task_counter < self.max_page_limit):
            if len(self.to_visit) > 0:
                next_url = self.to_visit.pop()
                self.visiting.add(next_url)

                tasks.append(asyncio.create_task(self.process_page(next_url)))
                task_counter +=1
            else:
                await asyncio.sleep(0) # Allow other tasks to run
        await asyncio.gather(*tasks)
        logger.info(f"{task_counter} pages crawled")
    
    def update_to_visit(self, urls):
        for url in urls:
            if url not in self.visited and url not in self.visiting:
                self.to_visit.add(url)
                logger.info(f"Adding URL to queue: {url}")
    
async def main():

    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("starting_url", help="Starting URL")
    parser.add_argument("max_page_limit", help="Max Page Limit", required=False)
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

if __name__ == "__main__":
    asyncio.run(main())