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
    
# defining inputs for the function
league_id = "419220233"
season_id = "2025"
team_id = "8"
espn_s2 = "AECrbCxSDYAsEOTBJQryjbMBUKLBexs8d8uHArXqmeHB6HbBUk0QgHCLiHkFCbixlYN9bIkaaF0W%2BNVR%2BXfeGqhZkR1zkEvUiS8aJOx61mq1KpxsXXiyg9V8Jzsk1A051FjurJUvSfOHv2WjgAeh0Mjxx%2FG%2FeLQYk8k0VJ1WsvOs6mf9UHEizoelxAnuC%2BiVYlL7GoIXIZnHwONkl2ml1I6Af1f%2FsyBfaVA35UXRHHD9lVJ8t92PHsKAIYiYlRYAqkO7I54rNdls%2FF2GttcL%2B242ARh86GCgsiewXprufIEmtQ%3D%3D" 
swid = "{EC688D8E-6470-412F-8C38-809400D9316B}"

# parsing through team data in league rankings
# if statement so this only runs if fetching team data is successful
if teams:
    def parse_team_data(teams):
        team_stats = []
        for team in teams.get("teams", []):
            team_stats.append({
                "Team Name": team.get("name"),
                "Abbreviation": team.get("abbrev"),
                "Projected Rank": team.get("currentProjectedRank"),
                "Points": team.get("points"),
                "Wins": team.get("record", {}).get("overall", {}).get("wins"),
                "Losses": team.get("record", {}).get("overall", {}).get("losses"),
                "Winning Percentage": team.get("record", {}).get("overall", {}).get("percentage"),
                "Logo": team.get("logo"),
            })
        return pd.DataFrame(team_stats)

# save all team data under a specific dataframe
    team_data_df = parse_team_data(teams)

# adding sidebar navigation menu with different options
st.sidebar.title("Navigation")
    view = st.sidebar.radio("Select View", ["Overview", "Team Details", "Visualizations"])

# league overview section
    if view == "Overview":
        st.header("League Overview")
        st.write("League Summary:")
        st.dataframe(team_data_df)


# selectbox creates dropdown menu
# user can select a team, stored under df selected_team
# still need to modify parameters e.g. pixel width
    elif view == "Team Details":
        st.header("Team Details")
        selected_team = st.selectbox("Select a team:", team_data_df["Team Name"])
        team_info = team_data_df[team_data_df["Team Name"] == selected_team].iloc[0]
        st.image(team_info["Logo"], width=100)
        st.write(f"**Team Name:** {team_info['Team Name']}")
        st.write(f"**Abbreviation:** {team_info['Abbreviation']}")
        st.write(f"**Projected Rank:** {team_info['Projected Rank']}")
        st.write(f"**Points:** {team_info['Points']}")
        st.write(f"**Wins:** {team_info['Wins']}")
        st.write(f"**Losses:** {team_info['Losses']}")
        st.write(f"**Winning Percentage:** {team_info['Winning Percentage']:.2%}")

# basic visualization section with plotly
# displays simple bar charts for now with league metrics
# more to be added
    elif view == "Visualizations":
        st.header("League Visualizations")

        st.subheader("Points by Team")
        fig = px.bar(
            team_data_df,
            x="Team Name",
            y="Points",
            title="Total Points by Team",
            labels={"Points": "Total Points", "Team Name": "Team"},
            hover_data=["Projected Rank", "Wins", "Losses"],
        )
        st.plotly_chart(fig)

        st.subheader("Winning Percentage by Team")
        fig = px.bar(
            team_data_df,
            x="Team Name",
            y="Winning Percentage",
            title="Winning Percentage by Team",
            labels={"Winning Percentage": "Winning Percentage", "Team Name": "Team"},
            hover_data=["Projected Rank", "Points", "Wins", "Losses"],
        )
        st.plotly_chart(fig)

# in case there is an issue loading team_data_df or accessing API
else:
    st.write("Unable to load data. Please check your credentials and try again.")

