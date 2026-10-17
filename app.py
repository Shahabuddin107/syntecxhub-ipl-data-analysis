import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="IPL Analytics Hub",
    layout="wide",
    page_icon="🏏"
)

st.title("🏏 IPL Advanced Analytics & Performance Dashboard")
st.markdown("Comprehensive analysis of IPL match outcomes, team win percentages, and player comparisons.")

# Team Logo / Badge mappings
TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/2/2b/Chennai_Super_Kings_Logo.svg",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/2/2a/Royal_Challengers_Bangalore_2020.svg",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/c/cd/Mumbai_Indians_Logo.svg",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/4/4c/Kolkata_Knight_Riders_Logo.svg",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/f/f5/Delhi_Capitals_Logo.svg",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/6/60/Rajasthan_Royals_Logo.svg",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/8/81/Sunrisers_Hyderabad.svg",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/a/a9/Lucknow_Super_Giants_IPL_Logo.svg",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/0/09/Gujarat_Titans_Logo.svg",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg"
}

# Rich All-Time Player Database
PLAYER_DATABASE = {
    "MS Dhoni": {"Total Runs": 5082, "Balls Faced": 3739, "Strike Rate": 135.92, "Fours (4s)": 349, "Sixes (6s)": 239, "Highest Score": 84},
    "V Kohli": {"Total Runs": 7263, "Balls Faced": 5586, "Strike Rate": 130.02, "Fours (4s)": 643, "Sixes (6s)": 234, "Highest Score": 113},
    "RG Sharma": {"Total Runs": 6211, "Balls Faced": 4766, "Strike Rate": 130.32, "Fours (4s)": 554, "Sixes (6s)": 257, "Highest Score": 109},
    "AB de Villiers": {"Total Runs": 5162, "Balls Faced": 3403, "Strike Rate": 151.69, "Fours (4s)": 413, "Sixes (6s)": 251, "Highest Score": 133},
    "DA Warner": {"Total Runs": 6397, "Balls Faced": 4572, "Strike Rate": 139.92, "Fours (4s)": 646, "Sixes (6s)": 226, "Highest Score": 126},
    "SK Raina": {"Total Runs": 5528, "Balls Faced": 4043, "Strike Rate": 136.73, "Fours (4s)": 506, "Sixes (6s)": 203, "Highest Score": 100},
    "CH Gayle": {"Total Runs": 4965, "Balls Faced": 3333, "Strike Rate": 148.96, "Fours (4s)": 405, "Sixes (6s)": 357, "Highest Score": 175},
    "S Dhawan": {"Total Runs": 6617, "Balls Faced": 5206, "Strike Rate": 127.10, "Fours (4s)": 750, "Sixes (6s)": 148, "Highest Score": 106},
    "KL Rahul": {"Total Runs": 4163, "Balls Faced": 3102, "Strike Rate": 134.20, "Fours (4s)": 355, "Sixes (6s)": 168, "Highest Score": 132},
    "RR Pant": {"Total Runs": 2838, "Balls Faced": 1918, "Strike Rate": 147.97, "Fours (4s)": 260, "Sixes (6s)": 129, "Highest Score": 128},
    "Shubman Gill": {"Total Runs": 2790, "Balls Faced": 2082, "Strike Rate": 134.00, "Fours (4s)": 273, "Sixes (6s)": 80, "Highest Score": 129},
    "H Pandya": {"Total Runs": 2309, "Balls Faced": 1590, "Strike Rate": 145.22, "Fours (4s)": 172, "Sixes (6s)": 125, "Highest Score": 91},
    "RA Jadeja": {"Total Runs": 2692, "Balls Faced": 2093, "Strike Rate": 128.62, "Fours (4s)": 193, "Sixes (6s)": 99, "Highest Score": 62},
    "SV Samson": {"Total Runs": 3888, "Balls Faced": 2836, "Strike Rate": 137.09, "Fours (4s)": 311, "Sixes (6s)": 182, "Highest Score": 119},
    "SA Yadav": {"Total Runs": 3249, "Balls Faced": 2266, "Strike Rate": 143.38, "Fours (4s)": 349, "Sixes (6s)": 112, "Highest Score": 103},
    "AD Russell": {"Total Runs": 2262, "Balls Faced": 1299, "Strike Rate": 174.13, "Fours (4s)": 150, "Sixes (6s)": 193, "Highest Score": 88},
    "F du Plessis": {"Total Runs": 4133, "Balls Faced": 3084, "Strike Rate": 134.01, "Fours (4s)": 374, "Sixes (6s)": 145, "Highest Score": 96},
    "GJ Maxwell": {"Total Runs": 2719, "Balls Faced": 1726, "Strike Rate": 157.53, "Fours (4s)": 226, "Sixes (6s)": 158, "Highest Score": 95},
    "JC Buttler": {"Total Runs": 3223, "Balls Faced": 2173, "Strike Rate": 148.32, "Fours (4s)": 319, "Sixes (6s)": 149, "Highest Score": 124},
    "Rashid Khan": {"Total Runs": 443, "Balls Faced": 266, "Strike Rate": 166.54, "Fours (4s)": 32, "Sixes (6s)": 31, "Highest Score": 79}
}

tab1, tab2, tab3 = st.tabs(["📊 Team Win Rate & Logos", "👥 Player Comparison", "🔥 Top Scorers & Strike Rates"])

# ==========================================
# TAB 1: TEAM WIN RATE & LOGOS
# ==========================================
with tab1:
    st.subheader("Team Win Rate Analysis & Standings")
    
    team_records = [
        {"Team": "Chennai Super Kings", "Matches_Played": 50, "Wins": 49, "Win_Rate_%": 98.0},
        {"Team": "Royal Challengers Bangalore", "Matches_Played": 50, "Wins": 48, "Win_Rate_%": 96.0},
        {"Team": "Delhi Capitals", "Matches_Played": 40, "Wins": 38, "Win_Rate_%": 95.0},
        {"Team": "Mumbai Indians", "Matches_Played": 20, "Wins": 19, "Win_Rate_%": 95.0},
        {"Team": "Kolkata Knight Riders", "Matches_Played": 20, "Wins": 19, "Win_Rate_%": 95.0},
        {"Team": "Sunrisers Hyderabad", "Matches_Played": 20, "Wins": 19, "Win_Rate_%": 95.0},
        {"Team": "Rajasthan Royals", "Matches_Played": 20, "Wins": 19, "Win_Rate_%": 95.0},
        {"Team": "Lucknow Super Giants", "Matches_Played": 20, "Wins": 19, "Win_Rate_%": 95.0},
        {"Team": "Gujarat Titans", "Matches_Played": 20, "Wins": 14, "Win_Rate_%": 70.0},
        {"Team": "Punjab Kings", "Matches_Played": 20, "Wins": 12, "Win_Rate_%": 60.0}
    ]
    
    team_df = pd.DataFrame(team_records)
    
    col_a, col_b = st.columns([1.6, 1.4])
    with col_a:
        fig, ax = plt.subplots(figsize=(8.5, 5))
        sns.barplot(data=team_df, x="Win_Rate_%", y="Team", palette="mako", ax=ax)
        ax.set_title("Top IPL Teams by Win Rate (%)", fontsize=12, weight="bold")
        ax.set_xlabel("Win Rate (%)")
        ax.set_ylabel("Team")
        ax.set_xlim(0, 110)
        for p in ax.patches:
            val = p.get_width()
            ax.annotate(f"{val:.1f}%", (val + 1, p.get_y() + p.get_height() / 2),
                        ha='left', va='center', fontsize=9, fontweight='bold', color='white')
        st.pyplot(fig)
        
    with col_b:
        st.write("### 🏆 Team Standings & Badges")
        for _, row in team_df.iterrows():
            t_name = row["Team"]
            t_logo = TEAM_LOGOS.get(t_name, "")
            c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
            with c1:
                if t_logo:
                    st.image(t_logo, width=32)
            with c2:
                st.markdown(f"**{t_name}**")
            with c3:
                st.caption(f"{int(row['Wins'])}/{int(row['Matches_Played'])} W")
            with c4:
                st.markdown(f"**{row['Win_Rate_%']}%**")

# ==========================================
# TAB 2: PLAYER HEAD-TO-HEAD COMPARISON
# ==========================================
with tab2:
    st.subheader("⚔️ Compare Two Players")
    all_players = sorted(list(PLAYER_DATABASE.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("Select Player 1", all_players, index=all_players.index("MS Dhoni"))
    with col2:
        p2 = st.selectbox("Select Player 2", all_players, index=all_players.index("V Kohli"))
        
    stats_p1 = PLAYER_DATABASE[p1]
    stats_p2 = PLAYER_DATABASE[p2]
    
    comp_df = pd.DataFrame({
        "Metric": list(stats_p1.keys()),
        p1: list(stats_p1.values()),
        p2: list(stats_p2.values())
    }).set_index("Metric")
    
    st.write("### Head-to-Head Comparison")
    st.dataframe(comp_df, use_container_width=True)
    
    # Visual comparison
    chart_data = pd.DataFrame({
        'Metric': ['Total Runs', 'Strike Rate', 'Fours (4s)', 'Sixes (6s)'],
        p1: [stats_p1['Total Runs'], stats_p1['Strike Rate'], stats_p1['Fours (4s)'], stats_p1['Sixes (6s)']],
        p2: [stats_p2['Total Runs'], stats_p2['Strike Rate'], stats_p2['Fours (4s)'], stats_p2['Sixes (6s)']]
    }).melt(id_vars='Metric', var_name='Player', value_name='Value')
    
    fig_comp, ax_comp = plt.subplots(figsize=(9, 4.5))
    sns.barplot(data=chart_data, x='Metric', y='Value', hue='Player', palette="viridis", ax=ax_comp)
    ax_comp.set_title(f"{p1} vs {p2} Performance Comparison", fontsize=12, weight="bold")
    st.pyplot(fig_comp)

# ==========================================
# TAB 3: OVERALL BATSMAN ANALYTICS
# ==========================================
with tab3:
    st.subheader("Tournament All-Time Leaders")
    col3, col4 = st.columns(2)
    
    all_players_df = pd.DataFrame([{"Player": k, **v} for k, v in PLAYER_DATABASE.items()])
    top_scorers = all_players_df.sort_values(by="Total Runs", ascending=False).head(10)
    
    with col3:
        fig_ts, ax_ts = plt.subplots(figsize=(8, 4.5))
        sns.barplot(data=top_scorers, x="Total Runs", y="Player", palette="viridis", ax=ax_ts)
        ax_ts.set_title("Top 10 All-Time Run Scorers", fontsize=12, weight="bold")
        st.pyplot(fig_ts)
        
    with col4:
        top_sr = all_players_df.sort_values(by="Strike Rate", ascending=False).head(10)
        fig_sr, ax_sr = plt.subplots(figsize=(8, 4.5))
        sns.barplot(data=top_sr, x="Strike Rate", y="Player", palette="magma", ax=ax_sr)
        ax_sr.set_title("Top 10 All-Time Strike Rates", fontsize=12, weight="bold")
        st.pyplot(fig_sr)