import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page styling
st.set_page_config(page_title="IPL Analytics Hub", layout="wide", page_icon="🏏")

st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Advanced Analytics & Performance Dashboard")
st.markdown("Comprehensive analysis of IPL match outcomes, team win percentages, and player comparisons.")

# Load datasets
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    matches = pd.read_csv(os.path.join(base_dir, "data", "matches.csv"))
    deliveries = pd.read_csv(os.path.join(base_dir, "data", "deliveries.csv"))
    return matches, deliveries

matches, deliveries = load_data()
batter_col = 'batter' if 'batter' in deliveries.columns else 'batsman'

# Top-level Tabs
tab1, tab2, tab3 = st.tabs(["📊 Team Win Rate & Matches", "👥 Player Comparison", "🔥 Top Scorers & Strike Rates"])

# ==========================================
# TAB 1: TEAM WIN RATE & METRICS
# ==========================================
with tab1:
    st.subheader("Team Win Rate Analysis")
    
    # Calculate matches played & wins for each team
    t1_played = matches['team1'].value_counts()
    t2_played = matches['team2'].value_counts()
    total_played = t1_played.add(t2_played, fill_value=0)
    
    wins = matches['winner'].value_counts()
    
    team_df = pd.DataFrame({'Matches_Played': total_played, 'Wins': wins}).dropna()
    team_df['Win_Rate_%'] = ((team_df['Wins'] / team_df['Matches_Played']) * 100).round(2)
    team_df = team_df.sort_values(by='Win_Rate_%', ascending=False)
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=team_df.head(10).reset_index(), x='Win_Rate_%', y='index', palette="coolwarm", ax=ax)
        ax.set_title("Top 10 Teams by Win Rate (%)", fontsize=12, weight="bold")
        ax.set_xlabel("Win Rate (%)")
        ax.set_ylabel("Team")
        st.pyplot(fig)
        
    with col_b:
        st.write("### Team Leaderboard")
        st.dataframe(team_df, use_container_width=True)

# ==========================================
# TAB 2: PLAYER HEAD-TO-HEAD COMPARISON
# ==========================================
with tab2:
    st.subheader("⚔️ Compare Two Players")
    all_players = sorted(deliveries[batter_col].dropna().unique().tolist())
    
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Select Player 1", all_players, index=all_players.index("V Kohli") if "V Kohli" in all_players else 0)
    with col2:
        player2 = st.selectbox("Select Player 2", all_players, index=all_players.index("MS Dhoni") if "MS Dhoni" in all_players else 1)
        
    def get_player_stats(player_name):
        p_df = deliveries[deliveries[batter_col] == player_name]
        runs = p_df['batsman_runs'].sum()
        balls = len(p_df)
        sr = round((runs / balls * 100), 2) if balls > 0 else 0
        fours = len(p_df[p_df['batsman_runs'] == 4])
        sixes = len(p_df[p_df['batsman_runs'] == 6])
        
        # High score in a single match
        match_id_col = 'match_id' if 'match_id' in p_df.columns else 'id'
        if match_id_col in p_df.columns:
            high_score = p_df.groupby(match_id_col)['batsman_runs'].sum().max()
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
    st.dataframe(comp_df.style.highlight_max(axis=1, color="#1e3a8a"), use_container_width=True)
    
    # Comparison Bar Chart
    fig_comp, ax_comp = plt.subplots(figsize=(10, 4))
    comp_chart_data = pd.DataFrame({
        'Metric': ['Total Runs', 'Strike Rate', 'Fours (4s)', 'Sixes (6s)'],
        player1: [p1_stats['Total Runs'], p1_stats['Strike Rate'], p1_stats['Fours (4s)'], p1_stats['Sixes (6s)']],
        player2: [p2_stats['Total Runs'], p2_stats['Strike Rate'], p2_stats['Fours (4s)'], p2_stats['Sixes (6s)']]
    }).melt(id_vars='Metric', var_name='Player', value_name='Value')
    
    sns.barplot(data=comp_chart_data, x='Metric', y='Value', hue='Player', palette="Set2", ax=ax_comp)
    ax_comp.set_title(f"{player1} vs {player2} Performance Comparison", fontsize=12, weight="bold")
    st.pyplot(fig_comp)

# ==========================================
# TAB 3: OVERALL BATSMAN ANALYTICS
# ==========================================
with tab3:
    st.subheader("Tournament All-Time Leaders")
    col3, col4 = st.columns(2)
    
    batsman_runs = deliveries.groupby(batter_col)['batsman_runs'].sum().reset_index()
    top_scorers = batsman_runs.sort_values(by='batsman_runs', ascending=False).head(10)
    
    with col3:
        fig_ts, ax_ts = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_scorers, x='batsman_runs', y=batter_col, palette="viridis", ax=ax_ts)
        ax_ts.set_title("Top 10 All-Time Run Scorers", fontsize=12, weight="bold")
        st.pyplot(fig_ts)
        
    with col4:
        balls = deliveries.groupby(batter_col)['ball'].count().reset_index(name='balls_faced')
        strike_df = pd.merge(batsman_runs, balls, on=batter_col)
        min_balls = 10 if len(deliveries) < 1000 else 500
        qualified = strike_df[strike_df['balls_faced'] >= min_balls].copy()
        qualified['strike_rate'] = (qualified['batsman_runs'] / qualified['balls_faced']) * 100
        top_sr = qualified.sort_values(by='strike_rate', ascending=False).head(10)
        
        fig_sr, ax_sr = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_sr, x='strike_rate', y=batter_col, palette="magma", ax=ax_sr)
        ax_sr.set_title(f"Top 10 Strike Rates (Min. {min_balls} Balls)", fontsize=12, weight="bold")
        st.pyplot(fig_sr)