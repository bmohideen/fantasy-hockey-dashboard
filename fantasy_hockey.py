# importing necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import requests

# creating function that fetches data for my fantasy league from the ESPN API
# league id, season_id, team_id are all specific to my team/league
# espn_s2 and swid: my own specific authentication cookies to access API
def fetch_fantasy_team_data(league_id, season_id, team_id, espn_s2, swid):
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/fhl/seasons/{season_id}/segments/0/leagues/{league_id}?view=mTeam&teamId={team_id}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"espn_s2={espn_s2}; SWID={swid}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None