import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="IPL Analytics Hub", layout="wide", page_icon="🏏")

st.title("🏏 IPL Advanced Analytics & Performance Dashboard")
st.markdown("Comprehensive analysis of IPL match outcomes, team win percentages, and player comparisons.")

# Load datasets
# Cache hata diya taaki real-time data update ho
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    matches = pd.read_csv(os.path.join(base_dir, "data", "matches.csv"))
    deliveries = pd.read_csv(os.path.join(base_dir, "data", "deliveries.csv"))
    return matches, deliveries

matches, deliveries = load_data()

# Column detection helper
def get_col(df, options):
    for opt in options:
        for col in df.columns:
            if opt.lower() == col.strip().lower():
                return col
    return None

winner_col = get_col(matches, ['winner', 'winning_team', 'match_winner'])
team1_col = get_col(matches, ['team1', 'team_1', 'team 1'])
team2_col = get_col(matches, ['team2', 'team_2', 'team 2'])
batter_col = get_col(deliveries, ['batter', 'batsman', 'player', 'striker'])
runs_col = get_col(deliveries, ['batsman_runs', 'batsman_run', 'runs_batter', 'runs'])
ball_col = get_col(deliveries, ['ball', 'ball_num', 'delivery'])
match_id_col = get_col(deliveries, ['match_id', 'id', 'matchId'])

# Default fallback agar exact match na mile
batter_col = batter_col if batter_col else deliveries.columns[0]
runs_col = runs_col if runs_col else deliveries.columns[-1]

# Tabs UI
tab1, tab2, tab3 = st.tabs(["📊 Team Win Rate & Matches", "👥 Player Comparison", "🔥 Top Scorers & Strike Rates"])

# ==========================================
# TAB 1: TEAM WIN RATE & METRICS
# ==========================================
with tab1:
    st.subheader("Team Win Rate Analysis")
    
    if winner_col:
        wins = matches[winner_col].dropna().value_counts()
        
        # Win rate calculate karein agar team1 aur team2 present ho
        if team1_col and team2_col:
            t1_played = matches[team1_col].value_counts()
            t2_played = matches[team2_col].value_counts()
            total_played = t1_played.add(t2_played, fill_value=0)
            team_df = pd.DataFrame({'Matches_Played': total_played, 'Wins': wins}).fillna(0)
            team_df['Win_Rate_%'] = ((team_df['Wins'] / team_df['Matches_Played'].replace(0, 1)) * 100).round(2)
            team_df = team_df.sort_values(by='Win_Rate_%', ascending=False)
            x_axis = 'Win_Rate_%'
            x_label = "Win Rate (%)"
        else:
            team_df = wins.reset_index()
            team_df.columns = ['Team', 'Wins']
            x_axis = 'Wins'
            x_label = "Total Wins"
            
        col_a, col_b = st.columns([2, 1])
        with col_a:
            fig, ax = plt.subplots(figsize=(9, 5))
            plot_df = team_df.head(10).reset_index()
            y_col = 'index' if 'index' in plot_df.columns else team_df.columns[0]
            sns.barplot(data=plot_df, x=x_axis, y=y_col, palette="coolwarm", ax=ax)
            ax.set_title(f"Top 10 Teams by {x_label}", fontsize=12, weight="bold")
            ax.set_xlabel(x_label)
            ax.set_ylabel("Team")
            st.pyplot(fig)
            
        with col_b:
            st.write("### Team Leaderboard")
            st.dataframe(team_df, use_container_width=True)
    else:
        st.warning("Matches dataset me winner column detect nahi hua.")

# ==========================================
# TAB 2: PLAYER HEAD-TO-HEAD COMPARISON
# ==========================================
with tab2:
    st.subheader("⚔️ Compare Two Players")
    all_players = sorted([str(p) for p in deliveries[batter_col].dropna().unique()])
    
    if len(all_players) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            idx1 = all_players.index("V Kohli") if "V Kohli" in all_players else 0
            player1 = st.selectbox("Select Player 1", all_players, index=idx1)
        with col2:
            idx2 = all_players.index("MS Dhoni") if "MS Dhoni" in all_players else 1
            player2 = st.selectbox("Select Player 2", all_players, index=idx2)
            
        def get_player_stats(player_name):
            p_df = deliveries[deliveries[batter_col] == player_name]
            runs = int(p_df[runs_col].sum()) if runs_col in p_df.columns else 0
            balls = len(p_df)
            sr = round((runs / balls * 100), 2) if balls > 0 else 0
            fours = int(len(p_df[p_df[runs_col] == 4])) if runs_col in p_df.columns else 0
            sixes = int(len(p_df[p_df[runs_col] == 6])) if runs_col in p_df.columns else 0
            
            if match_id_col and match_id_col in p_df.columns:
                high_score = int(p_df.groupby(match_id_col)[runs_col].sum().max())
            else:
                high_score = runs
                
            return {
                "Total Runs": runs,
                "Balls Faced": balls,
                "Strike Rate": sr,
                "Fours (4s)": fours,
                "Sixes (6s)": sixes,
                "Highest Match Score": high_score
            }
            
        p1_stats = get_player_stats(player1)
        p2_stats = get_player_stats(player2)
        
        comp_df = pd.DataFrame([p1_stats, p2_stats], index=[player1, player2]).T
        st.write("### Head-to-Head Comparison")
        st.dataframe(comp_df, use_container_width=True)
        
        fig_comp, ax_comp = plt.subplots(figsize=(10, 4))
        comp_chart_data = pd.DataFrame({
            'Metric': ['Total Runs', 'Strike Rate', 'Fours (4s)', 'Sixes (6s)'],
            player1: [p1_stats['Total Runs'], p1_stats['Strike Rate'], p1_stats['Fours (4s)'], p1_stats['Sixes (6s)']],
            player2: [p2_stats['Total Runs'], p2_stats['Strike Rate'], p2_stats['Fours (4s)'], p2_stats['Sixes (6s)']]
        }).melt(id_vars='Metric', var_name='Player', value_name='Value')
        
        sns.barplot(data=comp_chart_data, x='Metric', y='Value', hue='Player', palette="Set2", ax=ax_comp)
        ax_comp.set_title(f"{player1} vs {player2} Performance Comparison", fontsize=12, weight="bold")
        st.pyplot(fig_comp)
    else:
        st.info("Deliveries dataset me batsman data available nahi hai.")

# ==========================================
# TAB 3: OVERALL BATSMAN ANALYTICS
# ==========================================
with tab3:
    st.subheader("Tournament All-Time Leaders")
    col3, col4 = st.columns(2)
    
    batsman_runs = deliveries.groupby(batter_col)[runs_col].sum().reset_index()
    top_scorers = batsman_runs.sort_values(by=runs_col, ascending=False).head(10)
    
    with col3:
        fig_ts, ax_ts = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_scorers, x=runs_col, y=batter_col, palette="viridis", ax=ax_ts)
        ax_ts.set_title("Top 10 All-Time Run Scorers", fontsize=12, weight="bold")
        st.pyplot(fig_ts)
        
    with col4:
        balls = deliveries.groupby(batter_col).size().reset_index(name='balls_faced')
        strike_df = pd.merge(batsman_runs, balls, on=batter_col)
        min_balls = 10 if len(deliveries) < 1000 else 100
        qualified = strike_df[strike_df['balls_faced'] >= min_balls].copy()
        qualified['strike_rate'] = (qualified[runs_col] / qualified['balls_faced']) * 100
        top_sr = qualified.sort_values(by='strike_rate', ascending=False).head(10)
        
        fig_sr, ax_sr = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_sr, x='strike_rate', y=batter_col, palette="magma", ax=ax_sr)
        ax_sr.set_title(f"Top 10 Strike Rates (Min. {min_balls} Balls)", fontsize=12, weight="bold")
        st.pyplot(fig_sr)