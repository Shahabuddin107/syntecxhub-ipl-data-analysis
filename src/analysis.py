import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Datasets load karein
matches_path = os.path.join(DATA_DIR, "matches.csv")
deliveries_path = os.path.join(DATA_DIR, "deliveries.csv")

matches = pd.read_csv(matches_path)
deliveries = pd.read_csv(deliveries_path)

print(f"Loaded: {len(matches)} matches | {len(deliveries)} deliveries")
sns.set_theme(style="whitegrid")

# 1. Team Wins Chart
plt.figure(figsize=(10, 6))
top_teams = matches['winner'].value_counts().head(8).reset_index()
top_teams.columns = ['team', 'wins']
sns.barplot(data=top_teams, x='wins', y='team', hue='team', palette="viridis", legend=False)
plt.title("Top IPL Teams by Match Wins", fontsize=14, weight="bold")
plt.xlabel("Total Wins")
plt.ylabel("Team")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_teams_wins.png"), dpi=300)
plt.close()

# 2. Top Run Scorers Chart
batter_col = 'batter' if 'batter' in deliveries.columns else 'batsman'
batsman_runs = deliveries.groupby(batter_col)['batsman_runs'].sum().reset_index()
top_scorers = batsman_runs.sort_values(by='batsman_runs', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=top_scorers, x='batsman_runs', y=batter_col, hue=batter_col, palette="magma", legend=False)
plt.title("Top Run Scorers", fontsize=14, weight="bold")
plt.xlabel("Total Runs")
plt.ylabel("Batter")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_scorers.png"), dpi=300)
plt.close()

# 3. Strike Rate Chart
balls = deliveries.groupby(batter_col)['ball'].count().reset_index(name='balls_faced')
strike_df = pd.merge(batsman_runs, balls, on=batter_col)
# Qualification filter: real dataset ke liye 500 balls, demo ke liye 10
min_balls = 10 if len(deliveries) < 1000 else 500
qualified = strike_df[strike_df['balls_faced'] >= min_balls].copy()
qualified['strike_rate'] = (qualified['batsman_runs'] / qualified['balls_faced']) * 100
top_sr = qualified.sort_values(by='strike_rate', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=top_sr, x='strike_rate', y=batter_col, hue=batter_col, palette="rocket", legend=False)
plt.title(f"Highest Strike Rates (Min {min_balls} Balls Faced)", fontsize=14, weight="bold")
plt.xlabel("Strike Rate")
plt.ylabel("Batter")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_strike_rates.png"), dpi=300)
plt.close()

# 4. Season-wise Scoring Trend Chart
match_id_col = 'match_id' if 'match_id' in deliveries.columns else 'id'
merged = pd.merge(deliveries, matches[['id', 'season']], left_on=match_id_col, right_on='id')
season_runs = merged.groupby('season')['total_runs'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=season_runs, x='season', y='total_runs', marker='o', color='#E63946', linewidth=2.5)
plt.title("Season-wise Total Runs Trend", fontsize=14, weight="bold")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "season_run_trends.png"), dpi=300)
plt.close()

print("All charts generated and saved cleanly without warnings in 'outputs/'.")