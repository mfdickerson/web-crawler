"""
__main__.py

This script serves as the entry point for running the web crawler as a module.
It delegates execution to the main() function defined in src/web_crawler.py.
"""

import asyncio

from src.web_crawler import main

if __name__ == "__main__":
    asyncio.run(main())
