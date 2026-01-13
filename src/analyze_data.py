import pandas as pd


data = pd.read_csv('df_clean.csv')

# Descriptive statistics for numerical columns
descriptive_stats = data.describe()

# Calculate the correlation matrix
correlation_matrix = data[['halftime_home_goals', 'halftime_away_goals',
                           'fulltime_home_goals', 'fulltime_away_goals']].corr()

# Frequency of matches with total goals above a certain threshold
data['total_goals'] = data['home_goals'] + data['away_goals']
high_scoring_matches = data[data['total_goals'] > 5]

# Grouping data by year to identify scoring trends
scoring_trends = data.groupby('year')['total_goals'].mean()

print("Descriptive Statistics:")
print(descriptive_stats)

print("\nCorrelation Matrix:")
print(correlation_matrix)

print("\nNumber of High-Scoring Matches (Total Goals > 5):", high_scoring_matches.shape[0])

print("\nScoring Trends (Average Total Goals per Year):")
print(scoring_trends)




#team clean
team_data = pd.read_csv('team_clean.csv')

# Descriptive statistics for numeric columns
team_descriptive_stats = team_data[['GF', 'GA', 'xG']].describe()

# Win-Loss-Draw ratio
win_loss_draw = team_data['Result'].value_counts()

# Home vs. Away performance (average goals scored and conceded)
home_away_performance = team_data.groupby('Venue')[['GF', 'GA']].mean()

# Correlation between expected goals (xG) and goals scored (GF)
xg_gf_correlation = team_data[['xG', 'GF']].corr().loc['xG', 'GF']

# Scoring trends over the year
scoring_trends_team = team_data.groupby('year')[['GF', 'GA']].mean()

print("Descriptive Statistics:")
print(team_descriptive_stats)

print("\nWin-Loss-Draw Ratio:")
print(win_loss_draw)

print("\nHome vs. Away Performance (Average Goals Scored and Conceded):")
print(home_away_performance)

print("\nCorrelation between xG and GF:")
print(xg_gf_correlation)

print("\nScoring Trends by Year (Average GF and GA):")
print(scoring_trends_team)




#matches clean
matches_data = pd.read_csv('matches_clean.csv')

# Descriptive statistics for numeric columns
matches_descriptive_stats = matches_data.describe()

# Correlation matrix for numeric columns
matches_correlation_matrix = matches_data.corr()

# Performance trends by year (mean of numeric columns)
matches_trends_by_year = matches_data.groupby('year').mean()

print("Descriptive Statistics:")
print(matches_descriptive_stats)

print("\nCorrelation Matrix:")
print(matches_correlation_matrix)

print("\nPerformance Trends by Year:")
print(matches_trends_by_year)



#shooting
shooting_data = pd.read_csv('shooting_clean.csv')

# Descriptive statistics for numeric columns
shooting_descriptive_stats = shooting_data.describe()

# Correlation matrix for numeric columns
shooting_correlation_matrix = shooting_data.corr()

# Performance trends by year (mean of numeric columns)
shooting_trends_by_year = shooting_data.groupby('year').mean()

print("Descriptive Statistics:")
print(shooting_descriptive_stats)

print("\nCorrelation Matrix:")
print(shooting_correlation_matrix)

print("\nPerformance Trends by Year:")
print(shooting_trends_by_year)