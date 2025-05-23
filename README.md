# 🕷️ Web Crawler

An efficient and lightweight asynchronous web crawler built in Python. Given a starting URL, the crawler visits all pages within the same domain (and subdomain), printing each URL it visits and listing all the links found on that page.

The crawler is limited to a single subdomain — for example, if you start with `https://www.overstory.com/`, it will crawl all pages under `www.overstory.com` but will **not** follow external links (e.g., `blog.overstory.com` or `example.com`).

---

## Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
  - [Setup](#setup)
  - [Docker](#-docker)
  - [Example Output](#-example-output)
- [Contributing and Testing](#-contributing-and-testing)
- [License](#️-license)
- [Contact](#-contact)

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
web-crawler/
│
├── src/
│   ├── requirements/               # Requirements needed to run web crawler
│   │   ├── code_style.txt          # Requirements for code style checks
│   │   └── dev.txt                 # Requirements for development and running module
│   │
│   ├── tests/
│   │   ├── conftest.py             # Configurations shared between multiple unit test files
│   │   ├── test_page_parser.py     # Unit tests for PageParser class
│   │   └── test_web_crawler.py     # Unit tests for WebCrawler class
│   │
│   └── web_crawler.py              # Main crawler logic
│
├── tests/
│   └── integration/
│       ├── requirements.txt        # Requirements for running integration tests
│       └── test_web_crawler.py     # Integration tests
│
├── Dockerfile
├── LICENSE.md
├── README.md
├── CONTRIBUTING.md
└── __main__.py                     # Entry point for running the crawler
```

---

## 🔧 Usage

### Setup

Setting up virtual environment and installing dependancies:
```bash
cd src
virtualenv -p python3.13 venv && source venv/bin/activate
pip install -r requirements/dev.txt
```

From the `src/` directory, run the crawler with a starting URL:

```bash
python web_crawler.py <URL> [--max_page_limit=<100>]
```

Example:

```bash
python web_crawler.py https://www.spider-man.com --max_page_limit=100
```

It will:
- Crawl all pages under the `https://www.spider-man.com` subdomain
- Print each URL it visits
- Print all links found on each page
- Ignore any links that point to other domains or subdomains

### 🐳 Docker

You can also run the web crawler in a containerized environment using Docker.

#### 🏗️ Build the Docker Image

From the root of the project directory:

```bash
docker build -t web-crawler .
```

#### 🚀 Run the Crawler

Replace `<URL>` with your desired starting point:

```bash
docker run --rm web-crawler <URL> [--max_page_limit=<100>]
```

Example:

```bash
docker run --rm web-crawler https://www.spider-man.com --max_page_limit=100
```

### ✨ Example Output

```bash
- https://www.web-crawlers.com/
  - https://www.web-crawlers.com/peter-parker
  - https://www.web-crawlers.com/gwen-stacy
  - https://www.web-crawlers.com/miles-morales
  - https://www.web-crawlers.com/peni-parker
  - https://www.web-crawlers.com/miguel-ohara

- https://www.web-crawlers.com/peter-parker
  - https://www.web-crawlers.com/peter-parker/interests

  - https://www.web-crawlers.com/peter-parker/interests
    - https://www.web-crawlers.com/gwen-stacy
    - https://www.the-daily-bugle.com # ignored
    - https://www.oscorp.com # ignored

- https://www.web-crawlers.com/gwen-stacy
  - https://www.web-crawlers.com/gwen-stacy/interests
  - https://www.web-crawlers.com/gwen-stacy/spider-gwen
...
```

---

## 🧪 Contributing and Testing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## 🛡️ License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 📫 Contact

For questions, feedback, or feature requests, please open an issue in this repository.
