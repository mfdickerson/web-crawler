# 🕷️ Web Crawler

An efficient and lightweight asynchronous web crawler built in Python. Given a starting URL, the crawler visits all pages within the same domain (and subdomain), printing each URL it visits and listing all the links found on that page.

The crawler is limited to a single subdomain — for example, if you start with `https://www.overstory.com/`, it will crawl all pages under `www.overstory.com` but will **not** follow external links (e.g., `blog.overstory.com` or `example.com`).

---

## 🚀 Features

- Asynchronous crawling using `aiohttp` and `asyncio`
- HTML parsing via `BeautifulSoup`
- Filters links to only crawl within the starting subdomain
- Prints each visited URL and the links found on that page
- Graceful error handling and optional rate-limiting
- Fully tested with `pytest` and `pytest-asyncio`

---

## 📦 Requirements

- Python 3.13.3
- aiohttp >= 3.11.18
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- pytest >= 8.3.2
- pytest-asyncio >= 0.21.0

Install dependencies with:

```bash
pip install -r src/requirements.txt
```

---

## 📁 Project Structure

```
async-web-crawler/
│
├── src/
│   ├── __init__.py
│   ├── requirements.txt            # Requirements needed to run web crawler
│   ├── web_crawler.py              # Main crawler logic
│   └── tests/
│       ├── init__.py
│       └── test_web_crawler.py     # Unit tests
│
├── tests/
│   └── integration/
│       ├── init__.py
│       ├── requirements.txt
│       └── test_web_crawler.py     # Integration tests
│
├── LICENSE.md
├── README.md
├── CONTRIBUTING.md
└── main.py                         # Entry point for running the crawler
```

---

## 🔧 Usage

Run the crawler with a starting URL:

```bash
python main.py https://www.overstory.com/
```

It will:
- Crawl all pages under the `www.overstory.com` subdomain
- Print each URL it visits
- Print all links found on each page
- Ignore any links that point to other domains or subdomains

---


## 🐳 Docker

You can run the web crawler in a containerized environment using Docker.

### 🏗️ Build the Docker Image

From the root of the project directory:

```bash
docker build -t web-crawler .
```

### 🚀 Run the Crawler

Replace `<URL>` with your desired starting point:

```bash
docker run --rm web-crawler python src/web_crawler.py <URL>
```

Example:

```bash
docker run --rm web-crawler python src/web_crawler.py https://www.overstory.com/
```


---

## ✨ Example Output

```bash
Visiting: https://www.overstory.com/
Links found:
  - https://www.overstory.com/about
  - https://www.overstory.com/contact
  - https://external.com/news     # Ignored

Visiting: https://www.overstory.com/about
Links found:
  - https://www.overstory.com/
  - https://www.overstory.com/team
```

---

## 🛡️ License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 📫 Contact

For questions, feedback, or feature requests, please open an issue in this repository.
