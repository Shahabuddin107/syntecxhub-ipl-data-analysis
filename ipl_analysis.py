import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting style set karein
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 1. Datasets load karein
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

print("--- Data Summary ---")
print(f"Total Matches: {len(matches)}")
print(f"Total Balls Bowled: {len(deliveries)}")

# ---------------------------------------------------------
# Requirement 1: Team Win Rates & Most Successful Teams
# ---------------------------------------------------------
plt.figure()
win_counts = matches['winner'].value_counts().head(8)
sns.barplot(x=win_counts.values, y=win_counts.index, palette="viridis")
plt.title("Top IPL Teams by Total Wins", fontsize=14, weight='bold')
plt.xlabel("Number of Wins")
plt.ylabel("Team")
plt.tight_layout()
plt.savefig("top_teams_wins.png")
plt.show()

# ---------------------------------------------------------
# Requirement 2: Top Scorers in IPL History
# ---------------------------------------------------------
batsman_runs = deliveries.groupby('batter')['batsman_runs'].sum().reset_index()
top_scorers = batsman_runs.sort_values(by='batsman_runs', ascending=False).head(10)

plt.figure()
sns.barplot(x='batsman_runs', y='batter', data=top_scorers, palette="magma")
plt.title("Top 10 Run Scorers in IPL", fontsize=14, weight='bold')
plt.xlabel("Total Runs Scored")
plt.ylabel("Batsman")
plt.tight_layout()
plt.savefig("top_scorers.png")
plt.show()

# ---------------------------------------------------------
# Requirement 3: Strike Rates (Min. 500 balls faced)
# ---------------------------------------------------------
balls_faced = deliveries.groupby('batter')['ball'].count().reset_index()
balls_faced.rename(columns={'ball': 'balls_faced'}, inplace=True)

bat_stats = pd.merge(batsman_runs, balls_faced, on='batter')
qualified_batsmen = bat_stats[bat_stats['balls_faced'] >= 500].copy()
qualified_batsmen['strike_rate'] = (qualified_batsmen['batsman_runs'] / qualified_batsmen['balls_faced']) * 100

top_strike_rates = qualified_batsmen.sort_values(by='strike_rate', ascending=False).head(10)

plt.figure()
sns.barplot(x='strike_rate', y='batter', data=top_strike_rates, palette="rocket")
plt.title("Highest Strike Rates (Min. 500 Balls Faced)", fontsize=14, weight='bold')
plt.xlabel("Strike Rate")
plt.ylabel("Batsman")
plt.tight_layout()
plt.savefig("top_strike_rates.png")
plt.show()

# ---------------------------------------------------------
# Requirement 4: Season-wise Total Runs Trend
# ---------------------------------------------------------
# Matches aur Deliveries merge karein season analysis ke liye
merged_data = pd.merge(deliveries, matches[['id', 'season']], left_on='match_id', right_on='id')
season_runs = merged_data.groupby('season')['total_runs'].sum().reset_index()

plt.figure()
sns.lineplot(x='season', y='total_runs', data=season_runs, marker='o', color='crimson', linewidth=2.5)
plt.title("Total Runs Scored Across IPL Seasons", fontsize=14, weight='bold')
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("season_run_trends.png")
plt.show()