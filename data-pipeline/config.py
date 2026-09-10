import os
from dotenv import load_dotenv

load_dotenv()


HEADERS = {"X-Riot-Token": os.getenv("ROT_API_KEY")}

RANKS = {
    "CHALLENGER": "challengerleagues",
    "GRANDMASTER": "grandmasterleagues",
    "MASTER": "masterleagues",
}

REGIONS = ["euw1", "na1", "kr", "br1", "jp1", "la1", "la2", "oc1", "ru", "tr1"]
