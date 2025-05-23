"""
Pytest fixtures and settings for the unit tests.
"""

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture()
async def client_session():
    async with aiohttp.ClientSession(trust_env=True) as client_session:
        return client_session
