import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="IPL Data Analysis", layout="wide")

st.title("🏏 IPL / Sports Data Analysis Dashboard")
st.markdown("Exploratory Data Analysis of IPL Matches, Deliveries & Team Metrics")

# Data load function
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    matches_path = os.path.join(base_dir, "data", "matches.csv")
    deliveries_path = os.path.join(base_dir, "data", "deliveries.csv")
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    return matches, deliveries

try:
    matches, deliveries = load_data()
    batter_col = 'batter' if 'batter' in deliveries.columns else 'batsman'

    # Sidebar Filter
    st.sidebar.header("Navigation & Filters")
    teams = matches['winner'].dropna().unique().tolist()
    selected_team = st.sidebar.selectbox("Filter by Winner Team", ["All Teams"] + teams)

    # 1. Team Wins Chart
    st.subheader("1. Top IPL Teams by Total Wins")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    top_teams = matches['winner'].value_counts().head(8).reset_index()
    top_teams.columns = ['team', 'wins']
    sns.barplot(data=top_teams, x='wins', y='team', palette="viridis", ax=ax1)
    st.pyplot(fig1)

    # 2. Top Run Scorers & Strike Rates
    st.subheader("2. Batsman Performance Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top Run Scorers**")
        batsman_runs = deliveries.groupby(batter_col)['batsman_runs'].sum().reset_index()
        top_scorers = batsman_runs.sort_values(by='batsman_runs', ascending=False).head(10)
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_scorers, x='batsman_runs', y=batter_col, palette="magma", ax=ax2)
        st.pyplot(fig2)

    with col2:
        st.markdown("**Highest Strike Rates**")
        balls = deliveries.groupby(batter_col)['ball'].count().reset_index(name='balls_faced')
        strike_df = pd.merge(batsman_runs, balls, on=batter_col)
        min_balls = 10 if len(deliveries) < 1000 else 500
        qualified = strike_df[strike_df['balls_faced'] >= min_balls].copy()
        qualified['strike_rate'] = (qualified['batsman_runs'] / qualified['balls_faced']) * 100
        top_sr = qualified.sort_values(by='strike_rate', ascending=False).head(10)
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_sr, x='strike_rate', y=batter_col, palette="rocket", ax=ax3)
        st.pyplot(fig3)

except Exception as e:
    st.error(f"Error loading datasets: {e}")