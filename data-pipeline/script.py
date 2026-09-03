import requests
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
GRANDMASTER_URL = "https://euw1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"

ranks = {
    "CHALLENGER": "challengerleagues",
    "GRANDMASTER": "grandmasterleagues",
    "MASTER": "masterleagues",
}

regions = ["euw1", "na1", "kr", "br1", "jp1", "la1", "la2", "oc1", "ru", "tr1"]


def get_grandmaster_data(region, rank, queue_type, api_key):
    headers = {"X-Riot-Token": api_key}
    url = (
        f"https://{region}.api.riotgames.com/lol/league/v4/{rank}/by-queue/{queue_type}"
    )
    response = requests.get(url, headers=headers)
    print(response)
    return (
        response.json()
        if response.status_code == 200
        else "Failed to retrieve the data"
    )


games = get_grandmaster_data(
    "euw1", ranks["GRANDMASTER"], "RANKED_SOLO_5x5", os.getenv("API_KEY")
)

for game in games["entries"]:
    print(f"Summoner Name: {game['puuid']}, League Points: {game['leaguePoints']}")
