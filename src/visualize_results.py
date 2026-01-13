import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_clean = pd.read_csv("df_clean.csv")

# Goals Distribution
plt.figure(figsize=(12, 6))
sns.histplot(df_clean['home_goals'], bins=10, kde=True, color='blue', label='Home Goals', alpha=0.6)
sns.histplot(df_clean['away_goals'], bins=10, kde=True, color='red', label='Away Goals', alpha=0.6)
plt.title('Distribution of Home and Away Goals')
plt.xlabel('Goals')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Venue Performance
venue_performance = df_clean.groupby('venue_name')[['home_goals', 'away_goals']].mean().sort_values(by='home_goals', ascending=False)
venue_performance.plot(kind='bar', figsize=(12, 6))
plt.title('Average Goals Scored at Each Venue')
plt.ylabel('Average Goals')
plt.xlabel('Venue')
plt.xticks(rotation=45, ha='right')
plt.show()

# League-Wise Goals
league_goals = df_clean.groupby('league_name')[['home_goals', 'away_goals']].sum()
league_goals.plot(kind='bar', figsize=(10, 6))
plt.title('Total Goals Scored in Each League')
plt.ylabel('Total Goals')
plt.xlabel('League')
plt.xticks(rotation=45)
plt.show()

matches = pd.read_csv("matches_clean.csv")
# Distribution Plots
plt.figure(figsize=(12, 6))
for i, col in enumerate(['GF', 'GA', 'xG', 'xGA', 'Poss'], start=1):
    plt.subplot(2, 3, i)
    sns.histplot(matches[col].dropna(), kde=True, bins=10, color='blue')
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Venue Performance
venue_performance = matches.groupby('Venue')[['GF', 'GA']].mean()
venue_performance.plot(kind='bar', figsize=(8, 6))
plt.title('Home vs Away Performance (Goals For and Against)')
plt.ylabel('Average Goals')
plt.xticks(rotation=0)
plt.show()

# Correlation matrix
correlation_matrix = matches[['GF', 'GA', 'xG', 'xGA', 'Poss']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

shooting = pd.read_csv("shooting_clean.csv")

# Visualization of Goal-Scoring Efficiency
plt.figure(figsize=(12, 6))
for i, col in enumerate(['G/Sh', 'G/SoT'], start=1):
    plt.subplot(1, 2, i)
    sns.histplot(shooting[col].dropna(), kde=True, bins=10, color='green')
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Bar Chart for Shots and Targets
shooting_averages = shooting[['Sh', 'SoT', 'Gls']].mean()
shooting_averages.plot(kind='bar', figsize=(8, 6))
plt.title('Average Shots, Shots on Target, and Goals')
plt.ylabel('Average Count')
plt.xticks(rotation=0)
plt.show()

team = pd.read_csv("team_clean.csv")

# Home vs. Away Performance
venue_performance = team.groupby('Venue')[['GF', 'GA']].mean()
venue_performance.plot(kind='bar', figsize=(8, 6))
plt.title('Home vs Away Performance (Goals For and Against)')
plt.ylabel('Average Goals')
plt.xticks(rotation=0)
plt.show()

# Results Distribution
results_count = team['Result'].dropna().value_counts()
results_count.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 6), startangle=90, colors=['green', 'red', 'blue'])
plt.title('Match Results Distribution')
plt.ylabel('')  
plt.show()

# Opponent-Wise Performance
opponent_performance = team.groupby('Opponent')[['GF', 'GA']].mean().sort_values(by='GF', ascending=False)
opponent_performance.plot(kind='bar', figsize=(12, 6))
plt.title('Opponent-Wise Performance (Goals For and Against)')
plt.ylabel('Average Goals')
plt.xticks(rotation=45, ha='right')
plt.show()

combined_df = pd.merge(matches, shooting, on=['Comp', 'Round', 'Venue', 'Result', 'GF', 'GA', 'xG', 'year'])

plt.figure(figsize=(10, 6))
sns.boxplot(data=combined_df, x='Comp', y='GF', hue='Venue', palette='coolwarm')
plt.title('Performance (GF) by Competition and Venue', fontsize=14)
plt.xlabel('Competition', fontsize=12)
plt.ylabel('Goals For (GF)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Venue', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

data_2022 = pd.read_csv("Liverpool2022.csv")
data_2024 = pd.read_csv("Liverpool2024.csv")
top_5_2022 = data_2022[['player_name', 'goals']].sort_values(by='goals', ascending=False).head(5)
top_5_2024 = data_2024[['player_name', 'goals']].sort_values(by='goals', ascending=False).head(5)

top_5_2022['year'] = 2022
top_5_2024['year'] = 2024

combined_top_5_scorers = pd.concat([top_5_2024, top_5_2022]).sort_values(by='goals', ascending=False)
colors = ['blue' if year == 2024 else 'orange' for year in combined_top_5_scorers['year']]

plt.figure(figsize=(10, 6))
plt.bar(combined_top_5_scorers['player_name'], combined_top_5_scorers['goals'], color=colors, alpha=0.7)
plt.xlabel("Player Name")
plt.ylabel("Goals Scored")
plt.title("Top 5 Goal Scorers of 2022 and 2024")
plt.xticks(rotation=45, ha='right')
plt.legend(['2024 (Blue)', '2022 (Orange)'], loc='upper right', title='Year')
plt.tight_layout()
plt.show()