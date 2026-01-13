# Source - 1 : API

import pandas as pd
import json

with open('api_football.json', 'r') as file:
    json_data = json.load(file)

matches = json_data["response"]

flattened_data = []
for match in matches:
    flattened_data.append({
        "fixture_id": match["fixture"]["id"],
        "referee": match["fixture"]["referee"],
        "date": match["fixture"]["date"],
        "venue_name": match["fixture"]["venue"]["name"],
        "venue_city": match["fixture"]["venue"]["city"],
        "league_name": match["league"]["name"],
        "league_country": match["league"]["country"],
        "home_team": match["teams"]["home"]["name"],
        "away_team": match["teams"]["away"]["name"],
        "home_goals": match["goals"]["home"],
        "away_goals": match["goals"]["away"],
        "halftime_home_goals": match["score"]["halftime"]["home"],
        "halftime_away_goals": match["score"]["halftime"]["away"],
        "fulltime_home_goals": match["score"]["fulltime"]["home"],
        "fulltime_away_goals": match["score"]["fulltime"]["away"],
        "home_winner": match["teams"]["home"]["winner"],
        "away_winner": match["teams"]["away"]["winner"]
    })

df = pd.DataFrame(flattened_data)

df_clean = df.drop(columns=[
    'referee', 'venue_city', 'league_country', 'home_team', 'away_team', 'home_winner', 'away_winner'
])
df_clean['year'] = pd.to_datetime(df_clean['date']).dt.year
df_clean = df_clean.drop(columns=["date"])
df_clean.to_csv('df_clean.csv', index=False)
print("Clean API data file saved.")

# Source - 2 : Web Scraping

import pandas as pd

matches = pd.read_csv("matches.csv")

matches['year'] = pd.to_datetime(matches['Date']).dt.year
matches_clean= matches.drop(columns=['Date',"Time","Day","Notes", 'Attendance', 'Captain','Formation', "Opp Formation", "Referee","Match Report"])
matches_clean.to_csv("matches_clean.csv", index="False")

shooting = pd.read_csv("shooting.csv")
shooting['year'] = pd.to_datetime(shooting['Date']).dt.year
shooting_clean= shooting[['Round','Venue','Result','GF','GA','Opponent','xG','year']]
shooting.to_csv("shooting_clean.csv", index="False")

team_data = pd.read_csv("team_data.csv")
team_data['year'] = pd.to_datetime(team_data['Date']).dt.year
team_clean= team_data[['Round','Venue','Result','GF','GA','Opponent','xG','year']]
team_clean.to_csv("team_clean.csv", index="False")
print("3 clean data files saved")

# Source - 3 : SQL Database
import sqlite3
connection = sqlite3.connect('LiverpoolPlayerStats.db')  

liverpool2024_query = """
SELECT id, player_name, jersey_number, games_played, games_started, 
       goals, assists, shots, shots_on_target 
FROM LiverpoolPlayerStats2024
"""

liverpool2024_df = pd.read_sql_query(liverpool2024_query, connection)

liverpool2024_df.to_csv('Liverpool2024.csv', index=False)

liverpool2022_query = """
SELECT id, player_name, goals, assists, goals_assists 
FROM LiverpoolPlayerStats2022
"""

liverpool2022_df = pd.read_sql_query(liverpool2022_query, connection)

liverpool2022_df.to_csv('Liverpool2022.csv', index=False)

connection.close()

print("Data exported successfully to Liverpool2022.csv!")