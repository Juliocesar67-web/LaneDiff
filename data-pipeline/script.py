import requests
from dotenv import load_dotenv, dotenv_values
import os
import time
import asyncio
import httpx
import asyncpg

load_dotenv()
HEADERS = {"X-Riot-Token": os.getenv("API_KEY")}
SEMAPHORE = asyncio.Semaphore(10)
pause_until = time.time()  # Global variable to track the pause time for rate limiting
ranks = {
    "CHALLENGER": "challengerleagues",
    "GRANDMASTER": "grandmasterleagues",
    "MASTER": "masterleagues",
}

regions = ["euw1", "na1", "kr", "br1", "jp1", "la1", "la2", "oc1", "ru", "tr1"]


async def get_players(
    client: httpx.AsyncClient,
    region: str,
    rank: str,
    queue_type: str,
):
    url = (
        f"https://{region}.api.riotgames.com/lol/league/v4/{rank}/by-queue/{queue_type}"
    )

    response = await fetch_with_rate_limit(client, url, params={})
    print(response)
    return response


# function responsible for getting all the games from a player using their puuid
# fields:
# start-time (time window for the games, preferrably the day the patch comes out)
# end-time (time window for the games, preferrably the day the patch ends)
# queue_id (the queue id for the games, preferrably 420 for ranked solo)
# queue_type (the queue type for the games, preferrably ranked)
# start (the start index for the games, depends on which progress you are at from the game retrievals because of the rate limiters)
# count (the count of games to retrieve, maximum of 100)


async def get_games_from_player(
    client: httpx.AsyncClient, pool: asyncpg.Pool, puuid, params: dict
):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

    response = await fetch_with_rate_limit(client, url, params)
    print(response)
    if response is None:
        return []

    try:
        match_ids = await pool.execute(
            """
            INSERT INTO match_queue (id)
            SELECT * FROM unnest($1::text[])
            ON CONFLICT (id) DO NOTHING;
            """,
            response,
        )

    except Exception as e:
        print(f"Error inserting game in db: {e}")
    return response


async def fetch_with_rate_limit(client: httpx.AsyncClient, url: str, params: dict):
    """Executes GET requests with automatic HTTP 429 retry backoff."""
    global pause_until
    async with SEMAPHORE:
        while True:
            now = time.time()
            if now < pause_until:
                await asyncio.sleep(pause_until - now)
            try:
                response = await client.get(
                    url, headers=HEADERS, params=params, timeout=10.0
                )

                # Rate limited: read Riot's requested sleep duration and retry
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    pause_until = max(pause_until, time.time() + retry_after)
                    print(f"[429 Rate Limit] Backing off for {retry_after}s...")
                    await asyncio.sleep(retry_after)
                    continue

                if response.status_code == 200:
                    return response.json()

                print(f"API Error {response.status_code}: {response.text}")
                return None

            except httpx.RequestError as exc:
                print(f"Network error occurred: {exc}. Retrying in 2s...")
                await asyncio.sleep(2)


async def get_patch_dates(pool: asyncpg.Pool):
    try:
        patch_date = await pool.fetchrow(
            "SELECT start_time, end_time FROM patches WHERE is_current = true LIMIT 1"
        )
        print(f"Fetched patch date: {patch_date}")
        start_epoch = (
            int(patch_date["start_time"].timestamp())
            if patch_date is not None
            else None
        )
        end_epoch = (
            int(patch_date["end_time"].timestamp()) if patch_date is not None else None
        )
        return start_epoch, end_epoch
    except Exception as e:
        print(f"Error fetching patch date: {e}")
        start_epoch = None
        end_epoch = None
        return start_epoch, end_epoch


async def main():
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    start_epoch, end_epoch = await get_patch_dates(pool)
    async with httpx.AsyncClient() as client:
        chall_players = await get_players(
            client, "euw1", ranks["CHALLENGER"], "RANKED_SOLO_5x5"
        )

        if chall_players:
            tasks = [
                get_games_from_player(
                    client,
                    pool,
                    player["puuid"],
                    {
                        "startTime": start_epoch,
                        "endTime": end_epoch,
                        "queue": 420,
                        "type": "ranked",
                        "start": 0,
                        "count": 100,
                    },
                )
                for player in chall_players.get("entries", [])[:10]
            ]
            games_list = await asyncio.gather(*tasks)
            print(games_list)
            print(len(games_list))
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
