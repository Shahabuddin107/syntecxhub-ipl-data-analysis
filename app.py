import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import backend as bk

st.set_page_config(
    page_title="IPL Official Analytics Hub (2008-2026)",
    layout="wide",
    page_icon="🏏"
)

# 1. Initialize SQLite Backend Database
bk.init_database()

# 2. Fetch Clean Dynamic Data via Backend Queries
df_teams = bk.fetch_all_teams()
df_venues = bk.fetch_all_venues()
df_players = bk.fetch_all_players()
df_finals = bk.fetch_finals_history()

# 3. Broadcast Theme Dark UI Styling
st.markdown("""
<style>
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px solid #374151;
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 25px;
    }
    .ipl-header-logo {
        width: 85px;
        height: auto;
    }
    .header-text h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
    }
    .header-text p {
        margin: 4px 0 0 0;
        color: #94a3b8;
        font-size: 13px;
    }
    .team-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .rank-badge-1 {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #111;
        font-weight: 800;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
    }
    .rank-badge {
        background-color: #374151;
        color: #f3f4f6;
        font-weight: 700;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
    }
    .team-logo-img {
        width: 42px;
        height: 42px;
        object-fit: contain;
        margin-right: 12px;
    }
    .trophy-badge-container {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.25));
        border: 1px solid rgba(245, 158, 11, 0.6);
        padding: 3px 9px;
        border-radius: 12px;
        margin-left: 8px;
    }
    .trophy-icon-symbol {
        font-size: 15px;
        margin-right: 5px;
    }
    .trophy-text {
        color: #fcd34d;
        font-size: 11px;
        font-weight: 800;
    }
    .team-name {
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
    }
    .matches-subtext {
        font-size: 12px;
        color: #9ca3af;
    }
    .rate-val {
        font-size: 18px;
        font-weight: 800;
        color: #10b981;
    }
    .rate-label {
        font-size: 10px;
        color: #9ca3af;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

IPL_LOGO_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/500px-Indian_Premier_League_Official_Logo.svg.png"

st.markdown(f'<div class="header-container"><img src="{IPL_LOGO_URL}" class="ipl-header-logo" alt="IPL Logo" /><div class="header-text"><h1>Indian Premier League Official Analytics Hub (2008 – 2026)</h1><p>Full-Stack Analytics: SQLite Backend Database, ML Predictor, Stadium Insights & Player Metrics.</p></div></div>', unsafe_allow_html=True)

# 4. Multi-Section Analytical Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏆 Standings & Trophies",
    "⚡ All Teams Phase Breakdown",
    "🏟️ Stadium Analytics",
    "👥 Player Head-to-Head",
    "⚡ Strike Rate & Run Leaders",
    "🥇 Finals History",
    "🔮 ML Match Predictor"
])

# ==========================================
# TAB 1: STANDINGS
# ==========================================
with tab1:
    st.subheader("Official Standings (Powered by SQLite Backend)")
    col_l, col_r = st.columns([1.65, 1])
    with col_l:
        for _, t in df_teams.iterrows():
            badge_class = "rank-badge-1" if t["rank"] == 1 else "rank-badge"
            
            if t["is_winner"] == 1:
                trophy_badge_html = f'<span class="trophy-badge-container"><span class="trophy-icon-symbol">🏆</span><span class="trophy-text">{t["trophies_count"]}</span></span>'
            else:
                trophy_badge_html = f'<span style="background: rgba(156, 163, 175, 0.15); border: 1px solid #4b5563; padding: 2px 8px; border-radius: 12px; font-size: 11px; color: #9ca3af; margin-left: 8px;">{t["trophies_count"]}</span>'

            card_html = f'<div class="team-card" style="border-left: 6px solid {t["color"]};"><div style="display: flex; align-items: center;"><div class="{badge_class}">{t["rank"]}</div><img src="{t["logo"]}" class="team-logo-img" alt="{t["team"]}" /><div><div style="display: flex; align-items: center; flex-wrap: wrap;"><span class="team-name">{t["team"]}</span>{trophy_badge_html}</div><div class="matches-subtext">Matches: {t["played"]} | Won: {t["wins"]} | Lost: {t["losses"]} | Home: {t["venue"].split(",")[0]}</div></div></div><div style="text-align: right;"><div class="rate-val">{t["rate"]}%</div><div class="rate-label">Win Rate</div></div></div>'
            st.markdown(card_html, unsafe_allow_html=True)
            
    with col_r:
        fig, ax = plt.subplots(figsize=(6, 8.5))
        sns.barplot(data=df_teams, x="rate", y="short", palette="mako", ax=ax)
        ax.set_title("Win Rate % Comparison", fontsize=11, weight="bold")
        ax.set_xlim(0, 80)
        for p in ax.patches:
            val = p.get_width()
            ax.annotate(f"{val:.1f}%", (val + 1, p.get_y() + p.get_height() / 2),
                        ha='left', va='center', fontsize=9, fontweight='bold', color='white')
        st.pyplot(fig)

# ==========================================
# TAB 2: PHASE BREAKDOWN
# ==========================================
with tab2:
    st.subheader("⚡ 10 Franchises: Phase-by-Phase Scoring Rates")
    phase_table = df_teams[["team", "short", "powerplay_rr", "middle_rr", "death_rr"]].rename(
        columns={"powerplay_rr": "Powerplay (1-6)", "middle_rr": "Middle Overs (7-15)", "death_rr": "Death Overs (16-20)"}
    )
    st.dataframe(phase_table.set_index("team"), use_container_width=True)

# ==========================================
# TAB 3: STADIUM ANALYTICS
# ==========================================
with tab3:
    st.subheader("🏟️ Stadium Analytics (From SQLite Database)")
    st.dataframe(df_venues.set_index("stadium"), use_container_width=True)
    
    sel_venue = st.selectbox("Select Ground for Metrics:", df_venues["stadium"].tolist())
    target_v = df_venues[df_venues["stadium"] == sel_venue].iloc[0]
    
    c_v1, c_v2, c_v3 = st.columns(3)
    c_v1.metric("Total Matches Hosted", int(target_v["matches"]))
    c_v2.metric("Chasing Win %", f"{target_v['chase_win_pct']}%")
    c_v3.metric("Avg 1st Innings Score", int(target_v["avg_1st_innings"]))

# ==========================================
# TAB 4: PLAYER HEAD TO HEAD
# ==========================================
with tab4:
    st.subheader("👥 Compare Two Superstars (Backend Metrics)")
    all_players = df_players["player_name"].tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("Select Player 1", all_players, index=all_players.index("MS Dhoni"))
    with col2:
        p2 = st.selectbox("Select Player 2", all_players, index=all_players.index("Virat Kohli"))
        
    s1 = df_players[df_players["player_name"] == p1].iloc[0]
    s2 = df_players[df_players["player_name"] == p2].iloc[0]
    
    comp_df = pd.DataFrame({
        "Metric": ["Span", "Total Runs", "Balls Faced", "Strike Rate", "4s", "6s", "Highest Score", "Wickets"],
        p1: [s1["span"], s1["total_runs"], s1["balls"], s1["strike_rate"], s1["fours"], s1["sixes"], s1["highest_score"], s1["wickets"]],
        p2: [s2["span"], s2["total_runs"], s2["balls"], s2["strike_rate"], s2["fours"], s2["sixes"], s2["highest_score"], s2["wickets"]]
    }).set_index("Metric")
    
    st.dataframe(comp_df, use_container_width=True)

# ==========================================
# TAB 5: STRIKE RATE & RUN LEADERS
# ==========================================
with tab5:
    st.subheader("⚡ Batsmen Strike Rates & Historical Runs")
    col_lead1, col_lead2 = st.columns(2)
    with col_lead1:
        st.markdown("#### 🏏 Highest Strike Rates")
        top_sr = df_players.sort_values(by="strike_rate", ascending=False).head(10)
        fig_s, ax_s = plt.subplots(figsize=(7, 5))
        sns.barplot(data=top_sr, x="strike_rate", y="player_name", palette="magma", ax=ax_s)
        ax_s.set_xlim(0, 190)
        st.pyplot(fig_s)
        
    with col_lead2:
        st.markdown("#### 🏅 All-Time Highest Run Scorers")
        top_runs = df_players.sort_values(by="total_runs", ascending=False).head(10)
        fig_r, ax_r = plt.subplots(figsize=(7, 5))
        sns.barplot(data=top_runs, x="total_runs", y="player_name", palette="viridis", ax=ax_r)
        ax_r.set_xlim(0, 9000)
        st.pyplot(fig_r)

# ==========================================
# TAB 6: FINALS HISTORY
# ==========================================
with tab6:
    st.subheader("🥇 IPL Finals History: Champion Winners")
    st.dataframe(df_finals.set_index("season"), use_container_width=True)

# ==========================================
# TAB 7: ML PREDICTOR
# ==========================================
with tab7:
    st.subheader("🔮 Machine Learning Match Predictor (Powered by Backend Model)")
    team_list = df_teams["team"].tolist()
    
    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        team_a = st.selectbox("Team 1", team_list, index=0)
    with cp2:
        team_b = st.selectbox("Team 2", [t for t in team_list if t != team_a], index=0)
    with cp3:
        toss_winner = st.selectbox("Toss Winner Team", [team_a, team_b])
        
    prob_a, prob_b = bk.predict_match_outcome(team_a, team_b, toss_winner)
    
    st.markdown(f"#### 🏏 Live Win Probability: **{team_a}** vs **{team_b}**")
    m1, m2 = st.columns(2)
    m1.metric(label=f"{team_a} Projected Win Chance", value=f"{prob_a}%")
    m2.metric(label=f"{team_b} Projected Win Chance", value=f"{prob_b}%")
    st.progress(prob_a / 100)
