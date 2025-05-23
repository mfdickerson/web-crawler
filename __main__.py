import asyncio

from src.web_crawler import main

if __name__ == "__main__":
    # Entry point for the application.
    # Runs the asynchronous main() function from the web_crawler module.
    asyncio.run(main())
