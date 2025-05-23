"""
conftest.py

Shared pytest fixtures for integration tests.
Provides a mock HTTP server and an aiohttp client session.
"""

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture()
async def client_session():
    """Provides an aiohttp.ClientSession for testing."""
    async with aiohttp.ClientSession(trust_env=True) as client_session:
        return client_session
