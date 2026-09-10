import asyncio
import httpx
import asyncpg
import os

from riot_api import fetch_with_rate_limit


async def get_pending_matches(pool: asyncpg.Pool, count: int):
    try:
        pending_matches = await pool.fetch(
            "Select id FROM match_queue WHERE status = 'PENDING' LIMIT $1 FOR UPDATE SKIP LOCKED",
            count,
        )
        return pending_matches
    except Exception as e:
        print(f"Error fetching pending matches: {e}")
        return []


async def process_single_match(
    client: httpx.AsyncClient, pool: asyncpg.Pool, match_id: str
):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    match = await fetch_with_rate_limit(client, url, params={})
    if not match:
        print(f"Error fetching match details for {match_id}")
        return None
    while True:
        update_status = await update_match_status(pool, match_id, "COMPLETED")
        if not update_status:
            print(
                f"Error updating match status for {match_id}. Retrying in 5 seconds..."
            )
            await asyncio.sleep(5)
            continue
        break
    return match


async def update_match_status(pool: asyncpg.Pool, match_id: str, status: str):
    try:
        await pool.execute(
            "UPDATE match_queue SET status = $1 WHERE id = $2", status, match_id
        )
        return True
    except Exception as e:
        print(f"[DB Error] Could not update status to {status} for {match_id}: {e}")


async def match_details_worker(client: httpx.AsyncClient, pool: asyncpg.Pool):
    while True:
        pending_matches = await get_pending_matches(pool, count=10)
        if not pending_matches:
            print("No pending matches found. Waiting for 10 seconds...")
            break

        tasks = [
            process_single_match(client, pool, match["id"]) for match in pending_matches
        ]
        match_details_list = await asyncio.gather(*tasks)
        print(match_details_list)


async def main():
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"), min_size=5, max_size=15)


if __name__ == "__main__":
    asyncio.run(main())
