import os
from src.lol.time_conversions import *
import requests
import pandas as pd
import time
from src.utils import print_error, print_info


class RiotRateLimit(Exception):
    pass


def exponential_retry(func):
    # Wait 1, 2, 4, 8, 16, 32, 64, 128
    # 8 times
    def wrapper(*args, **kwargs):
        for i in range(8):
            try:
                return func(*args, **kwargs)
            except RiotRateLimit:
                print_error(f"Got rate limited, retrying {func.__name__} in {2 ** i} seconds...")
                time.sleep(2 ** i)
            except Exception:
                raise
        raise Exception("Tried 10 times, cannot get data. Check if the API key is valid or if the server is down.")

    return wrapper


@exponential_retry
def get_puuid(summoner_name: str, region: str):
    base_url = f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": os.getenv("LEAGUE_API_KEY")
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("puuid")
    elif response.status_code == 429:
        raise RiotRateLimit("Got rate limited.")

    raise Exception(f"Cannot get puuid, check if the summoner "
                    f"name is correct or if the API key is valid. Error: {response.json()}")


def get_match_history(puuid: str, start_time: str, end_time: str):
    start_timestamp = date_to_timestamp_start(start_time)
    end_timestamp = date_to_timestamp_end(end_time)

    start = 0
    count = 100

    match_history = []
    while True:
        @exponential_retry
        def _get_match_history():
            base_url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}"
                        f"&count={count}&startTime={start_timestamp}&endTime={end_timestamp}")
            headers = {
                "X-Riot-Token": os.getenv("LEAGUE_API_KEY"),
            }

            response = requests.get(base_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data
            elif response.status_code == 429:
                raise RiotRateLimit("Got rate limited.")

            raise Exception(f"Cannot get match history, check if the summoner "
                            f"name is correct or if the API key is valid. Error: {response.json()}")

        new_match_history = _get_match_history()
        print_info(f"Got {len(new_match_history)} more matches.")

        if len(new_match_history) == 0:
            break
        else:
            match_history += new_match_history
            start += count

    return match_history


def filter_match_data(match_data: dir, puuid: str):
    filtered_data = {
        "id": match_data["metadata"]["matchId"],
        "start_time": timestamp_milis_to_datetime(match_data["info"]["gameStartTimestamp"]),
        "stop_time": timestamp_milis_to_datetime(match_data["info"]["gameEndTimestamp"]),
        "duration_in_seconds": match_data["info"]["gameDuration"],
        "duration_in_minutes": match_data["info"]["gameDuration"] / 60,
        "gamemode": match_data["info"]["gameMode"],
        "kda_formatted": None,
        "kda": None,
        "win": None,
        "champion": None,
    }

    for player in match_data["info"]["participants"]:
        if player["puuid"] == puuid:
            filtered_data["kda_formatted"] = f"{player['kills']}/{player['deaths']}/{player['assists']}"
            player["deaths"] = 1 if player["deaths"] == 0 else player["deaths"]
            filtered_data["kda"] = (player["kills"] + player["assists"]) / player["deaths"]
            filtered_data["win"] = player["win"]
            filtered_data["champion"] = player["championName"]
            break

    return filtered_data


@exponential_retry
def get_match_data(match_id: str):
    base_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": os.getenv("LEAGUE_API_KEY"),
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        print_info(f"Got match data for {match_id}")
        data = response.json()
        return data
    elif response.status_code == 429:
        raise RiotRateLimit("Got rate limited.")

    raise Exception(f"Cannot get match data, check rate limits or if the API key is valid. Error: {response.json()}")


def turn_data_to_dataframe(match_ids: list[dir], puuid: str):
    matches_data = [get_match_data(match_id) for match_id in match_ids]
    filtered_matches_data = [filter_match_data(match_data, puuid) for match_data in matches_data]

    return pd.DataFrame(filtered_matches_data)
