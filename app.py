import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="IPL Official Analytics Hub (2008-2026)",
    layout="wide",
    page_icon="🏏"
)

# Dark Broadcast Styling
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
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .ipl-header-logo {
        width: 85px;
        height: auto;
        filter: drop-shadow(0px 3px 6px rgba(0, 0, 0, 0.6));
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
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease;
    }
    .team-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
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
        font-size: 13px;
        margin-right: 12px;
        flex-shrink: 0;
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
        font-size: 12px;
        margin-right: 12px;
        flex-shrink: 0;
    }
    .team-logo-img {
        width: 42px;
        height: 42px;
        object-fit: contain;
        margin-right: 12px;
        filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5));
    }
    .trophy-tag {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 2px 8px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 8px;
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

st.markdown(f"""
<div class="header-container">
    <img src="{IPL_LOGO_URL}" class="ipl-header-logo" alt="IPL Logo" />
    <div class="header-text">
        <h1>Indian Premier League Official Analytics Hub (2008 – 2026)</h1>
        <p>Franchise standings, trophy titles & final opponents, head-to-head metrics, match predictor, and superstar hall of fame.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 10 Official Teams Data with Trophy Details
TEAMS_DATA = [
    {
        "rank": 1, "team": "Chennai Super Kings", "short": "CSK",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/5G8eFjkPKNalIgL2FOtovg_500x500.png",
        "played": 239, "wins": 138, "losses": 98, "nr": 3, "rate": 58.47, "color": "#facc15", "trophies": "🏆 x5 (2010, '11, '18, '21, '23)"
    },
    {
        "rank": 2, "team": "Mumbai Indians", "short": "MI",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HmiWb77BmJDs6sHvn77v_Q_500x500.png",
        "played": 261, "wins": 144, "losses": 113, "nr": 4, "rate": 56.03, "color": "#0284c7", "trophies": "🏆 x5 (2013, '15, '17, '19, '20)"
    },
    {
        "rank": 3, "team": "Kolkata Knight Riders", "short": "KKR",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/bV4wF2dFs6IPc2BMtjgGZw_500x500.png",
        "played": 252, "wins": 130, "losses": 117, "nr": 5, "rate": 52.63, "color": "#7c3aed", "trophies": "🏆 x3 (2012, '14, '24)"
    },
    {
        "rank": 4, "team": "Gujarat Titans", "short": "GT",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/aTE8G7q-OcAobWvDd6sizQ_500x500.png",
        "played": 45, "wins": 28, "losses": 17, "nr": 0, "rate": 62.22, "color": "#1e293b", "trophies": "🏆 x1 (2022)"
    },
    {
        "rank": 5, "team": "Lucknow Super Giants", "short": "LSG",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/OqrL0ztLy13FBpvuF6GCBQ_500x500.png",
        "played": 44, "wins": 24, "losses": 19, "nr": 1, "rate": 55.81, "color": "#06b6d4", "trophies": "Playoffs ('22, '23)"
    },
    {
        "rank": 6, "team": "Rajasthan Royals", "short": "RR",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/GqIU6xhQAnCpy_Cbr2LZRA_500x500.png",
        "played": 222, "wins": 110, "losses": 106, "nr": 6, "rate": 50.93, "color": "#ec4899", "trophies": "🏆 x1 (2008)"
    },
    {
        "rank": 7, "team": "Royal Challengers Bengaluru", "short": "RCB",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/xUS54-BA0dFZPMtbCiHkzQ_500x500.png",
        "played": 256, "wins": 121, "losses": 128, "nr": 7, "rate": 48.59, "color": "#ef4444", "trophies": "Runners-up ('09, '11, '16)"
    },
    {
        "rank": 8, "team": "Sunrisers Hyderabad", "short": "SRH",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/W0OCBYc05c5MFMrctF62kg_500x500.png",
        "played": 182, "wins": 87, "losses": 91, "nr": 4, "rate": 48.88, "color": "#f97316", "trophies": "🏆 x1 (2016)"
    },
    {
        "rank": 9, "team": "Delhi Capitals", "short": "DC",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HzUX6_c8j7pwBCetmct2FQ_500x500.png",
        "played": 252, "wins": 112, "losses": 134, "nr": 6, "rate": 45.53, "color": "#3b82f6", "trophies": "Runners-up ('20)"
    },
    {
        "rank": 10, "team": "Punjab Kings", "short": "PBKS",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/XUAb4iA3XozYbH_cXQCryQ_500x500.png",
        "played": 246, "wins": 109, "losses": 133, "nr": 4, "rate": 45.04, "color": "#dc2626", "trophies": "Runners-up ('14)"
    }
]

# All-Time IPL Finals History (Season, Winner, Runner-Up/Against, Margin, Venue)
IPL_FINALS_HISTORY = [
    {"Season": 2024, "Winner": "Kolkata Knight Riders", "Defeated (Against)": "Sunrisers Hyderabad", "Margin": "8 wickets", "Venue": "Chennai"},
    {"Season": 2023, "Winner": "Chennai Super Kings", "Defeated (Against)": "Gujarat Titans", "Margin": "5 wickets (DLS)", "Venue": "Ahmedabad"},
    {"Season": 2022, "Winner": "Gujarat Titans", "Defeated (Against)": "Rajasthan Royals", "Margin": "7 wickets", "Venue": "Ahmedabad"},
    {"Season": 2021, "Winner": "Chennai Super Kings", "Defeated (Against)": "Kolkata Knight Riders", "Margin": "27 runs", "Venue": "Dubai"},
    {"Season": 2020, "Winner": "Mumbai Indians", "Defeated (Against)": "Delhi Capitals", "Margin": "5 wickets", "Venue": "Dubai"},
    {"Season": 2019, "Winner": "Mumbai Indians", "Defeated (Against)": "Chennai Super Kings", "Margin": "1 run", "Venue": "Hyderabad"},
    {"Season": 2018, "Winner": "Chennai Super Kings", "Defeated (Against)": "Sunrisers Hyderabad", "Margin": "8 wickets", "Venue": "Mumbai"},
    {"Season": 2017, "Winner": "Mumbai Indians", "Defeated (Against)": "Rising Pune Supergiant", "Margin": "1 run", "Venue": "Hyderabad"},
    {"Season": 2016, "Winner": "Sunrisers Hyderabad", "Defeated (Against)": "Royal Challengers Bangalore", "Margin": "8 runs", "Venue": "Bengaluru"},
    {"Season": 2015, "Winner": "Mumbai Indians", "Defeated (Against)": "Chennai Super Kings", "Margin": "41 runs", "Venue": "Kolkata"},
    {"Season": 2014, "Winner": "Kolkata Knight Riders", "Defeated (Against)": "Kings XI Punjab", "Margin": "3 wickets", "Venue": "Bengaluru"},
    {"Season": 2013, "Winner": "Mumbai Indians", "Defeated (Against)": "Chennai Super Kings", "Margin": "23 runs", "Venue": "Kolkata"},
    {"Season": 2012, "Winner": "Kolkata Knight Riders", "Defeated (Against)": "Chennai Super Kings", "Margin": "5 wickets", "Venue": "Chennai"},
    {"Season": 2011, "Winner": "Chennai Super Kings", "Defeated (Against)": "Royal Challengers Bangalore", "Margin": "58 runs", "Venue": "Chennai"},
    {"Season": 2010, "Winner": "Chennai Super Kings", "Defeated (Against)": "Mumbai Indians", "Margin": "22 runs", "Venue": "Mumbai"},
    {"Season": 2009, "Winner": "Deccan Chargers", "Defeated (Against)": "Royal Challengers Bangalore", "Margin": "6 runs", "Venue": "Johannesburg"},
    {"Season": 2008, "Winner": "Rajasthan Royals", "Defeated (Against)": "Chennai Super Kings", "Margin": "3 wickets", "Venue": "Navi Mumbai"}
]

# Team Trophy Aggregation (Total titles & list of beaten teams)
TEAM_TROPHY_SUMMARY = [
    {"Team": "Chennai Super Kings", "Titles": 5, "Years Won": "2010, 2011, 2018, 2021, 2023", "Finals Won Against": "MI (2010), RCB (2011), SRH (2018), KKR (2021), GT (2023)"},
    {"Team": "Mumbai Indians", "Titles": 5, "Years Won": "2013, 2015, 2017, 2019, 2020", "Finals Won Against": "CSK (2013, '15, '19), RPS (2017), DC (2020)"},
    {"Team": "Kolkata Knight Riders", "Titles": 3, "Years Won": "2012, 2014, 2024", "Finals Won Against": "CSK (2012), PBKS/KXIP (2014), SRH (2024)"},
    {"Team": "Sunrisers Hyderabad / DC", "Titles": 2, "Years Won": "2009, 2016", "Finals Won Against": "RCB (2009 as Deccan Chargers), RCB (2016 as SRH)"},
    {"Team": "Rajasthan Royals", "Titles": 1, "Years Won": "2008", "Finals Won Against": "CSK (2008)"},
    {"Team": "Gujarat Titans", "Titles": 1, "Years Won": "2022", "Finals Won Against": "RR (2022)"}
]

# Head-to-Head Data
H2H_DATA = {
    "Chennai Super Kings": [
        {"Opponent": "Mumbai Indians", "Played": 36, "Won": 16, "Lost": 20},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 32, "Won": 21, "Lost": 10},
        {"Opponent": "Kolkata Knight Riders", "Played": 29, "Won": 19, "Lost": 10},
        {"Opponent": "Delhi Capitals", "Played": 30, "Won": 19, "Lost": 11},
        {"Opponent": "Rajasthan Royals", "Played": 29, "Won": 16, "Lost": 13},
        {"Opponent": "Sunrisers Hyderabad", "Played": 20, "Won": 15, "Lost": 5},
        {"Opponent": "Punjab Kings", "Played": 29, "Won": 16, "Lost": 13},
        {"Opponent": "Gujarat Titans", "Played": 6, "Won": 3, "Lost": 3},
        {"Opponent": "Lucknow Super Giants", "Played": 5, "Won": 2, "Lost": 3}
    ],
    "Mumbai Indians": [
        {"Opponent": "Chennai Super Kings", "Played": 36, "Won": 20, "Lost": 16},
        {"Opponent": "Kolkata Knight Riders", "Played": 32, "Won": 23, "Lost": 9},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 34, "Won": 20, "Lost": 14},
        {"Opponent": "Delhi Capitals", "Played": 34, "Won": 19, "Lost": 15},
        {"Opponent": "Rajasthan Royals", "Played": 29, "Won": 15, "Lost": 14},
        {"Opponent": "Sunrisers Hyderabad", "Played": 22, "Won": 13, "Lost": 9},
        {"Opponent": "Punjab Kings", "Played": 31, "Won": 16, "Lost": 15},
        {"Opponent": "Gujarat Titans", "Played": 5, "Won": 2, "Lost": 3},
        {"Opponent": "Lucknow Super Giants", "Played": 5, "Won": 1, "Lost": 4}
    ]
}

# Bowlers All-Time Database
BOWLERS_DATA = [
    {"Player": "Yuzvendra Chahal", "Wickets": 205, "Matches": 160, "Economy": 7.66, "Best": "5/40"},
    {"Player": "Piyush Chawla", "Wickets": 192, "Matches": 192, "Economy": 7.96, "Best": "4/17"},
    {"Player": "Dwayne Bravo", "Wickets": 183, "Matches": 161, "Economy": 8.38, "Best": "4/22"},
    {"Player": "Bhuvneshwar Kumar", "Wickets": 181, "Matches": 176, "Economy": 7.56, "Best": "5/19"},
    {"Player": "Sunil Narine", "Wickets": 180, "Matches": 177, "Economy": 6.73, "Best": "5/19"},
    {"Player": "Ravichandran Ashwin", "Wickets": 180, "Matches": 212, "Economy": 7.12, "Best": "4/34"},
    {"Player": "Jasprit Bumrah", "Wickets": 165, "Matches": 133, "Economy": 7.30, "Best": "5/10"},
    {"Player": "Rashid Khan", "Wickets": 149, "Matches": 121, "Economy": 6.82, "Best": "4/24"}
]

# Tabs Configuration
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏆 Official Standings & Trophies",
    "🥇 IPL Finals History (All Winners vs Against)",
    "⚔️ Head-to-Head",
    "🎯 Bowlers Analytics",
    "🧢 Orange & Purple Caps",
    "🔮 Match Predictor"
])

# ==========================================
# TAB 1: STANDINGS
# ==========================================
with tab1:
    st.subheader("All-Time Standings & Championship Titles (2008 – 2026)")
    col_l, col_r = st.columns([1.6, 1])
    with col_l:
        for t in TEAMS_DATA:
            badge_class = "rank-badge-1" if t["rank"] == 1 else "rank-badge"
            card_html = f"""
            <div class="team-card" style="border-left: 6px solid {t['color']};">
                <div style="display: flex; align-items: center;">
                    <div class="{badge_class}">{t['rank']}</div>
                    <img src="{t['logo']}" class="team-logo-img" alt="{t['team']}" />
                    <div>
                        <div style="display: flex; align-items: center;">
                            <span class="team-name">{t['team']}</span>
                            <span class="trophy-tag">{t['trophies']}</span>
                        </div>
                        <div class="matches-subtext">Matches: {t['played']} | Won: {t['wins']} | Lost: {t['losses']} | NR: {t['nr']}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div class="rate-val">{t['rate']}%</div>
                    <div class="rate-label">Win Rate</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    with col_r:
        df_teams = pd.DataFrame(TEAMS_DATA)
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
# TAB 2: IPL FINALS HISTORY (WINNERS VS AGAINST)
# ==========================================
with tab2:
    st.subheader("🥇 Kis Team Ne Kitni Trophy Jeeti & Kiske Against Jeeti")
    
    st.markdown("#### 🏆 Franchise Championship Summary")
    st.dataframe(pd.DataFrame(TEAM_TROPHY_SUMMARY).set_index("Team"), use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 📜 Complete Final Matches History (2008 – Present)")
    finals_df = pd.DataFrame(IPL_FINALS_HISTORY)
    st.dataframe(finals_df.set_index("Season"), use_container_width=True)

# ==========================================
# TAB 3: HEAD TO HEAD
# ==========================================
with tab3:
    st.subheader("Head-to-Head Matrix")
    team_names = [t["team"] for t in TEAMS_DATA]
    sel_team = st.selectbox("Select Team:", team_names, index=0)
    data_list = H2H_DATA.get(sel_team, H2H_DATA["Chennai Super Kings"])
    h_df = pd.DataFrame(data_list)
    h_df["Win %"] = ((h_df["Won"] / h_df["Played"]) * 100).round(2)
    st.dataframe(h_df.set_index("Opponent"), use_container_width=True)

# ==========================================
# TAB 4: BOWLERS
# ==========================================
with tab4:
    st.subheader("🎯 IPL All-Time Leading Wicket Takers")
    b_df = pd.DataFrame(BOWLERS_DATA)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.dataframe(b_df.set_index("Player"), use_container_width=True)
    with c2:
        fig_b, ax_b = plt.subplots(figsize=(6, 4.5))
        sns.barplot(data=b_df, x="Wickets", y="Player", palette="rocket", ax=ax_b)
        ax_b.set_title("Most Wickets in IPL History", fontsize=11, weight="bold")
        st.pyplot(fig_b)

# ==========================================
# TAB 5: CAPS
# ==========================================
with tab5:
    st.subheader("🧢 Legendary Cap Holders")
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        st.markdown("### 🟠 Top Orange Cap Records (Most Runs in a Season)")
        orange_df = pd.DataFrame([
            {"Season": 2016, "Batter": "Virat Kohli", "Runs": 973, "Team": "RCB"},
            {"Season": 2023, "Batter": "Shubman Gill", "Runs": 890, "Team": "GT"},
            {"Season": 2022, "Batter": "Jos Buttler", "Runs": 863, "Team": "RR"},
            {"Season": 2016, "Batter": "David Warner", "Runs": 848, "Team": "SRH"},
            {"Season": 2018, "Batter": "Kane Williamson", "Runs": 735, "Team": "SRH"}
        ])
        st.dataframe(orange_df.set_index("Season"), use_container_width=True)
    with col_cap2:
        st.markdown("### 🟣 Top Purple Cap Records (Most Wickets in a Season)")
        purple_df = pd.DataFrame([
            {"Season": 2021, "Bowler": "Harshal Patel", "Wickets": 32, "Team": "RCB"},
            {"Season": 2013, "Bowler": "Dwayne Bravo", "Wickets": 32, "Team": "CSK"},
            {"Season": 2020, "Bowler": "Kagiso Rabada", "Wickets": 30, "Team": "DC"},
            {"Season": 2023, "Bowler": "Mohammed Shami", "Wickets": 28, "Team": "GT"},
            {"Season": 2022, "Bowler": "Yuzvendra Chahal", "Wickets": 27, "Team": "RR"}
        ])
        st.dataframe(purple_df.set_index("Season"), use_container_width=True)

# ==========================================
# TAB 6: MATCH PREDICTOR
# ==========================================
with tab6:
    st.subheader("🔮 IPL Match Outcome Predictor")
    st.markdown("Simulate win probability based on all-time head-to-head records & toss dynamics.")
    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        team_a = st.selectbox("Select Team 1", team_names, index=0)
    with cp2:
        team_b = st.selectbox("Select Team 2", [t for t in team_names if t != team_a], index=0)
    with cp3:
        toss_winner = st.selectbox("Toss Winner", [team_a, team_b])
    
    rate_a = next(t["rate"] for t in TEAMS_DATA if t["team"] == team_a)
    rate_b = next(t["rate"] for t in TEAMS_DATA if t["team"] == team_b)
    toss_boost = 3.5
    prob_a = round(((rate_a + (toss_boost if toss_winner == team_a else -toss_boost)) / (rate_a + rate_b)) * 100, 1)
    prob_b = round(100 - prob_a, 1)
    
    st.markdown(f"#### 🏏 Win Probability: **{team_a}** vs **{team_b}**")
    m1, m2 = st.columns(2)
    m1.metric(label=f"{team_a} Win Chance", value=f"{prob_a}%")
    m2.metric(label=f"{team_b} Win Chance", value=f"{prob_b}%")
    st.progress(prob_a / 100)