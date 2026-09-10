import os
import asyncio
import httpx
import asyncpg

from config import RANKS
from riot_api import fetch_with_rate_limit


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
    all_match_ids = []
    start_index = params.get("start", 0)
    batch_size = min(params.get("count", 100), 100)
    request_params = params.copy()
    request_params["count"] = batch_size
    while True:
        request_params["start"] = start_index
        response = await fetch_with_rate_limit(client, url, request_params)
        if not response:
            return []
        print(f"start count:{request_params['start']}.{response}")
        try:
            await pool.execute(
                """
                INSERT INTO match_queue (id)
                SELECT * FROM unnest($1::text[])
                ON CONFLICT (id) DO NOTHING;
                """,
                response,
            )
        except Exception as e:
            print(f"Error inserting game in db: {e}")

        all_match_ids.extend(response)
        if len(response) < batch_size:
            break
        start_index += batch_size

    return all_match_ids


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
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"), min_size=5, max_size=15)
    start_epoch, end_epoch = await get_patch_dates(pool)
    print(f"Start epoch: {start_epoch}, End epoch: {end_epoch}")
    async with httpx.AsyncClient() as client:
        chall_players = await get_players(
            client, "euw1", RANKS["CHALLENGER"], "RANKED_SOLO_5x5"
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
                for player in chall_players.get("entries", [])
            ]
            games_list = await asyncio.gather(*tasks)
            print(games_list)
            print(len(games_list))
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
