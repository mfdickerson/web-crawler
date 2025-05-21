import aiohttp
import requests
import asyncio
# import async_timeout
from bs4 import BeautifulSoup

import aiohttp
import asyncio
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]


class WebCrawler:

    def __init__(self, root_url, session):
        self.session = session
        self.root_url = root_url
        self.site_data = {}
        self.visited = set()
        self.to_visit = set([root_url])
        self.visiting = set()

    def print_site_data(self):
        for key, value in self.site_data.items():
            print(f"{key}")
            for link in value:
                print(f"  - {link}")
            print("\n")


    async def get_page(self, url):
        # with async_timeout.timeout(10):
        headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]}
        async with self.session.get(url, headers=headers) as response:
            page = await response.text()
            return page
        
    async def parse_page(self, url):
        print(f"start: {url}")
        page = await self.get_page(url)
        beautiful_page = BeautifulSoup(page, "html.parser")
        links = self.get_links(beautiful_page)
        self.site_data.update({url: links})

        new_urls = self.get_subdomains(links)
        self.update_to_visit(new_urls)
        self.visiting.remove(url)
        self.visited.add(url)
        print(f"end:   {url}")



    async def crawl(self):
        tasks = []
        while len(self.to_visit) > 0 or len(self.visiting) > 0:
            if len(self.to_visit) > 0:
                next_url = self.to_visit.pop()
                self.visiting.add(next_url)

                tasks.append(asyncio.create_task(self.parse_page(next_url)))
            else:
                await asyncio.sleep(0) # Allow other tasks to run
        await asyncio.gather(*tasks)
        
    def get_links(self, beautiful_page):
        links = beautiful_page.select("a[href]")
        return_urls = set()
        for link in links:
            url = link["href"]

            # convert links to absolute URLs
            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(self.root_url, url)
            else:
                absolute_url = url

            return_urls.add(absolute_url)

        return return_urls

    def get_subdomains(self, links):
        return_urls = []
        for link in links:
            # ensure the crawled link belongs to the target domain
            if link.startswith(self.root_url):
                return_urls.append(link)

        return return_urls
    
    def update_to_visit(self, urls):
        for url in urls:
            if url not in self.visited and url not in self.visiting:
                self.to_visit.add(url)
    
async def main():

    async with aiohttp.ClientSession(trust_env=True) as client_session:
        root_url = input("Enter a valid URL: ")
        web_crawler = WebCrawler(root_url, client_session)

        await web_crawler.crawl()

    web_crawler.print_site_data()


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())