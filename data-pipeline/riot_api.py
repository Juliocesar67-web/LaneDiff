import asyncio
import time
import httpx
from config import HEADERS

SEMAPHORE = asyncio.Semaphore(10)
pause_until = 0.0


async def fetch_with_rate_limit(
    client: httpx.AsyncClient, url: str, params: dict = None, max_retries: int = 3
):
    """Executes GET requests with automatic HTTP 429 retry backoff."""
    global pause_until
    if params is None:
        params = {}

        retries = 0
    async with SEMAPHORE:
        while retries < max_retries:
            now = time.time()
            if now < pause_until:
                await asyncio.sleep(pause_until - now)

            try:
                response = await client.get(
                    url, headers=HEADERS, params=params, timeout=10.0
                )

                if response.status_code == 200:
                    return response.json()

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    pause_until = max(pause_until, time.time() + retry_after)
                    print(f"[429 Rate Limit] Backing off for {retry_after}s...")
                    await asyncio.sleep(retry_after)
                    continue

                if 400 <= response.status_code < 500:
                    print(
                        f"[Permanent Error {response.status_code}] Abandoning request for {url}"
                    )
                    return None

                print(f"API Error {response.status_code}: {response.text}")
                return None

            except httpx.RequestError as exc:
                print(f"Network error occurred: {exc}. Retrying in 2s...")
                retries += 1
                await asyncio.sleep(2)
