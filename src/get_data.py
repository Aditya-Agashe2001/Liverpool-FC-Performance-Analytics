# Source - 1 : API

import requests
import json
import os

url = "https://v3.football.api-sports.io/fixtures?season=2022&team=40"
headers = {
    "x-rapidapi-key": "3f83a2a8e75c1dd8e82b160551a99421",  
    "x-rapidapi-host": "v3.football.api-sports.io"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  

    save_path = os.path.join(os.getcwd(), "api_football.json")  

    with open(save_path, "w") as json_file:
        json.dump(data, json_file, indent=4)  
        print(f"Data saved to {save_path}")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print("Response:", response.text)

# Source - 2 : Web Scraping

import requests
from bs4 import BeautifulSoup
import pandas as pd

standing_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

data = requests.get(standing_url)
soup = BeautifulSoup(data.text, features="lxml")  

standing_table = soup.select("table.stats_table")[0]
links = standing_table.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

team_url = team_urls[0]
data = requests.get(team_url)

try:
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]  
except ValueError as e:
    print("Error reading matches table:", e)
    matches = None

if matches is not None:
    soup = BeautifulSoup(data.text, features="lxml") 
    links = soup.find_all("a")
    links = [l.get("href") for l in links]
    links = [l for l in links if l and "all_comps/shooting/" in l]

    if links:
        data = requests.get(f"https://fbref.com{links[0]}")
        try:
            shooting = pd.read_html(data.text, match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()  

            team_data = matches.merge(
                shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]],
                on="Date",
                how="left"  
            )
            print("Web scraping complete!")
            if matches is not None:
                matches.to_csv("matches.csv", index=False)  
                print("Matches data saved to 'matches.csv'.")

            if 'shooting' in locals() and shooting is not None:
                shooting.to_csv("shooting.csv", index=False)  
                print("Shooting data saved to 'shooting.csv'.")

            if 'team_data' in locals() and team_data is not None:
                team_data.to_csv("team_data.csv", index=False)  
                print("Team data saved to 'team_data.csv'.")

        except ValueError as e:
            print("Error reading shooting data:", e)
    else:
        print("No shooting links found.")
else:
    print("No matches table found.")

# Source - 3 : SQL Database

import sqlite3

conn = sqlite3.connect('LiverpoolPlayerStats.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS LiverpoolPlayerStats2024 (
    id INTEGER PRIMARY KEY, 
    player_name TEXT NOT NULL, 
    jersey_number INTEGER NOT NULL, 
    games_played INTEGER NOT NULL, 
    games_started INTEGER NOT NULL, 
    goals INTEGER NOT NULL, 
    assists INTEGER NOT NULL,
    shots INTEGER NOT NULL, 
    shots_on_target INTEGER NOT NULL
);
""")

cursor.executemany("""
INSERT INTO LiverpoolPlayerStats2024 
(player_name, jersey_number, games_played, games_started, goals, assists, shots, shots_on_target) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", [
    ('Mohamed Salah', 11, 15, 15, 13, 9, 43, 28),
    ('L. Díaz', 7, 15, 10, 5, 2, 16, 10),
    ('C. Gakpo', 18, 15, 7, 3, 1, 16, 8),
    ('D. Szoboszlai', 8, 15, 11, 1, 1, 12, 7),
    ('C. Jones', 17, 12, 7, 2, 1, 8, 7),
    ('D. Núñez', 9, 12, 6, 2, 2, 13, 7),
    ('A. Mac Allister', 10, 14, 12, 0, 0, 8, 5),
    ('Diogo Jota', 20, 8, 7, 3, 2, 11, 4),
    ('V. van Dijk', 4, 15, 15, 1, 1, 9, 3),
    ('R. Gravenberch', 38, 15, 15, 0, 1, 5, 2),
    ('A. Robertson', 26, 14, 13, 0, 0, 3, 2),
    ('T. Alexander-Arnold', 66, 14, 13, 0, 3, 9, 2),
    ('I. Konaté', 5, 12, 11, 1, 1, 6, 2),
    ('C. Bradley', 84, 7, 1, 0, 0, 3, 2),
    ('J. Gomez', 2, 6, 3, 0, 0, 3, 2)
])

cursor.execute("""
CREATE TABLE IF NOT EXISTS LiverpoolPlayerStats2022 (
    id INTEGER PRIMARY KEY, 
    player_name TEXT NOT NULL, 
    goals INTEGER NOT NULL, 
    assists INTEGER NOT NULL, 
    goals_assists INTEGER NOT NULL
);
""")

cursor.executemany("""
INSERT INTO LiverpoolPlayerStats2022 
(player_name, goals, assists, goals_assists) 
VALUES (?, ?, ?, ?);
""", [
    ('Mohamed Salah', 7, 5, 12),
    ('Darwin Núñez', 5, 1, 6),
    ('Roberto Firmino', 4, 2, 6),
    ('Harvey Elliott', 2, 2, 4),
    ('Andrew Robertson', 0, 2, 2),
    ('Kostas Tsimikas', 0, 2, 2),
    ('Joe Gomez', 0, 1, 1),
    ('Jordan Henderson', 0, 1, 1),
    ('Thiago Alcántara', 0, 0, 0),
    ('Luis Díaz', 1, 0, 1),
    ('Diogo Jota', 0, 4, 4),
    ('Ibrahima Konaté', 0, 0, 0),
    ('James Milner', 0, 0, 0),
    ('Joël Matip', 1, 0, 1),
    ('Cody Gakpo', 0, 0, 0),
    ('Fabio Carvalho', 0, 0, 0),
    ('Stefan Bajcetic', 0, 0, 0),
    ('Curtis Jones', 0, 0, 0),
    ('Alex Oxlade-Chamberlain', 0, 0, 0),
    ('Arthur Melo', 0, 0, 0),
    ('Calvin Ramsay', 0, 0, 0)
])

print("LiverpoolPlayerStats2022 table created and populated successfully!")

conn.commit()
'''
cursor.execute("SELECT * FROM LiverpoolPlayerStats2024")
rows = cursor.fetchall()

# Display the data
for row in rows:
    print(row)'''
conn.close()

print("2024 Database and table created successfully!")