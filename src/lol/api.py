import os
from src.lol.time_conversions import *
import requests
import pandas as pd


def get_puuid(summoner_name: str, region: str):
    base_url = f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": os.getenv("LEAGUE_API_KEY")
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("puuid")

    raise Exception("Cannot get puuid, check if the summoner "
                    "name is correct or if the API key is valid.")


def get_match_history(puuid: str, start_time: str, end_time: str, start: int, count: int):
    start_timestamp = date_to_timestamp_start(start_time)
    end_timestamp = date_to_timestamp_end(end_time)

    base_url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}"
                f"&count={count}&startTime={start_timestamp}&endTime={end_timestamp}")
    headers = {
        "X-Riot-Token": os.getenv("LEAGUE_API_KEY"),
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    raise Exception(f"Cannot get match history, check if the summoner "
                    f"name is correct or if the API key is valid. Error: {response.json()}")


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


def get_match_data(match_id: str):
    base_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": os.getenv("LEAGUE_API_KEY"),
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    raise Exception("Cannot get match data, check rate limits or if the API key is valid.")


def turn_data_to_dataframe(match_ids: list[dir], puuid: str):
    matches_data = [get_match_data(match_id) for match_id in match_ids]
    filtered_matches_data = [filter_match_data(match_data, puuid) for match_data in matches_data]

    return pd.DataFrame(filtered_matches_data)
