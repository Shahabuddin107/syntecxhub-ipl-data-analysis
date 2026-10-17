import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="IPL All-Time Analytics Hub (2008-2026)",
    layout="wide",
    page_icon="🏏"
)

# Broadcast Style Dark Theme CSS
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
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
    }
    .header-text p {
        margin: 4px 0 0 0;
        color: #94a3b8;
        font-size: 14px;
    }
    .team-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
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
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        margin-right: 14px;
        flex-shrink: 0;
    }
    .rank-badge {
        background-color: #374151;
        color: #f3f4f6;
        font-weight: 700;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        margin-right: 14px;
        flex-shrink: 0;
    }
    .team-logo-img {
        width: 44px;
        height: 44px;
        object-fit: contain;
        margin-right: 14px;
        filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5));
    }
    .team-name {
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
    }
    .matches-subtext {
        font-size: 12px;
        color: #9ca3af;
    }
    .rate-val {
        font-size: 20px;
        font-weight: 800;
        color: #10b981;
    }
    .rate-label {
        font-size: 11px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Official IPL Header with Tournament Logo
IPL_LOGO_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/500px-Indian_Premier_League_Official_Logo.svg.png"

st.markdown(f"""
<div class="header-container">
    <img src="{IPL_LOGO_URL}" class="ipl-header-logo" alt="IPL Logo" />
    <div class="header-text">
        <h1>Indian Premier League Official Analytics Hub (2008 – 2026)</h1>
        <p>Comprehensive franchise standings, head-to-head records, win rates, and all-time superstar statistics.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 10 Official Teams Data
TEAMS_DATA = [
    {
        "rank": 1,
        "team": "Chennai Super Kings",
        "short": "CSK",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/5G8eFjkPKNalIgL2FOtovg_500x500.png",
        "played": 239, "wins": 138, "losses": 98, "nr": 3, "rate": 58.47, "color": "#facc15"
    },
    {
        "rank": 2,
        "team": "Mumbai Indians",
        "short": "MI",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HmiWb77BmJDs6sHvn77v_Q_500x500.png",
        "played": 261, "wins": 144, "losses": 113, "nr": 4, "rate": 56.03, "color": "#0284c7"
    },
    {
        "rank": 3,
        "team": "Kolkata Knight Riders",
        "short": "KKR",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/bV4wF2dFs6IPc2BMtjgGZw_500x500.png",
        "played": 252, "wins": 130, "losses": 117, "nr": 5, "rate": 52.63, "color": "#7c3aed"
    },
    {
        "rank": 4,
        "team": "Gujarat Titans",
        "short": "GT",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/aTE8G7q-OcAobWvDd6sizQ_500x500.png",
        "played": 45, "wins": 28, "losses": 17, "nr": 0, "rate": 62.22, "color": "#1e293b"
    },
    {
        "rank": 5,
        "team": "Lucknow Super Giants",
        "short": "LSG",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/OqrL0ztLy13FBpvuF6GCBQ_500x500.png",
        "played": 44, "wins": 24, "losses": 19, "nr": 1, "rate": 55.81, "color": "#06b6d4"
    },
    {
        "rank": 6,
        "team": "Rajasthan Royals",
        "short": "RR",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/GqIU6xhQAnCpy_Cbr2LZRA_500x500.png",
        "played": 222, "wins": 110, "losses": 106, "nr": 6, "rate": 50.93, "color": "#ec4899"
    },
    {
        "rank": 7,
        "team": "Royal Challengers Bengaluru",
        "short": "RCB",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/xUS54-BA0dFZPMtbCiHkzQ_500x500.png",
        "played": 256, "wins": 121, "losses": 128, "nr": 7, "rate": 48.59, "color": "#ef4444"
    },
    {
        "rank": 8,
        "team": "Sunrisers Hyderabad",
        "short": "SRH",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/W0OCBYc05c5MFMrctF62kg_500x500.png",
        "played": 182, "wins": 87, "losses": 91, "nr": 4, "rate": 48.88, "color": "#f97316"
    },
    {
        "rank": 9,
        "team": "Delhi Capitals",
        "short": "DC",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HzUX6_c8j7pwBCetmct2FQ_500x500.png",
        "played": 252, "wins": 112, "losses": 134, "nr": 6, "rate": 45.53, "color": "#3b82f6"
    },
    {
        "rank": 10,
        "team": "Punjab Kings",
        "short": "PBKS",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/XUAb4iA3XozYbH_cXQCryQ_500x500.png",
        "played": 246, "wins": 109, "losses": 133, "nr": 4, "rate": 45.04, "color": "#dc2626"
    }
]

# Head-to-Head Dataset (2008-2026)
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
    ],
    "Royal Challengers Bengaluru": [
        {"Opponent": "Chennai Super Kings", "Played": 32, "Won": 10, "Lost": 21},
        {"Opponent": "Mumbai Indians", "Played": 34, "Won": 14, "Lost": 20},
        {"Opponent": "Kolkata Knight Riders", "Played": 33, "Won": 14, "Lost": 19},
        {"Opponent": "Delhi Capitals", "Played": 30, "Won": 18, "Lost": 11},
        {"Opponent": "Rajasthan Royals", "Played": 30, "Won": 15, "Lost": 13},
        {"Opponent": "Sunrisers Hyderabad", "Played": 23, "Won": 11, "Lost": 12},
        {"Opponent": "Punjab Kings", "Played": 31, "Won": 15, "Lost": 16},
        {"Opponent": "Gujarat Titans", "Played": 4, "Won": 2, "Lost": 2},
        {"Opponent": "Lucknow Super Giants", "Played": 4, "Won": 3, "Lost": 1}
    ],
    "Kolkata Knight Riders": [
        {"Opponent": "Mumbai Indians", "Played": 32, "Won": 9, "Lost": 23},
        {"Opponent": "Chennai Super Kings", "Played": 29, "Won": 10, "Lost": 19},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 33, "Won": 19, "Lost": 14},
        {"Opponent": "Delhi Capitals", "Played": 32, "Won": 17, "Lost": 14},
        {"Opponent": "Rajasthan Royals", "Played": 29, "Won": 14, "Lost": 14},
        {"Opponent": "Sunrisers Hyderabad", "Played": 27, "Won": 18, "Lost": 9},
        {"Opponent": "Punjab Kings", "Played": 32, "Won": 21, "Lost": 11},
        {"Opponent": "Gujarat Titans", "Played": 3, "Won": 1, "Lost": 2},
        {"Opponent": "Lucknow Super Giants", "Played": 4, "Won": 1, "Lost": 3}
    ],
    "Delhi Capitals": [
        {"Opponent": "Chennai Super Kings", "Played": 30, "Won": 11, "Lost": 19},
        {"Opponent": "Mumbai Indians", "Played": 34, "Won": 15, "Lost": 19},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 30, "Won": 11, "Lost": 18},
        {"Opponent": "Kolkata Knight Riders", "Played": 32, "Won": 14, "Lost": 17},
        {"Opponent": "Rajasthan Royals", "Played": 28, "Won": 13, "Lost": 15},
        {"Opponent": "Sunrisers Hyderabad", "Played": 23, "Won": 11, "Lost": 12},
        {"Opponent": "Punjab Kings", "Played": 32, "Won": 16, "Lost": 16},
        {"Opponent": "Gujarat Titans", "Played": 4, "Won": 2, "Lost": 2},
        {"Opponent": "Lucknow Super Giants", "Played": 4, "Won": 1, "Lost": 3}
    ],
    "Rajasthan Royals": [
        {"Opponent": "Chennai Super Kings", "Played": 29, "Won": 13, "Lost": 16},
        {"Opponent": "Mumbai Indians", "Played": 29, "Won": 14, "Lost": 15},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 30, "Won": 13, "Lost": 15},
        {"Opponent": "Kolkata Knight Riders", "Played": 29, "Won": 14, "Lost": 14},
        {"Opponent": "Delhi Capitals", "Played": 28, "Won": 15, "Lost": 13},
        {"Opponent": "Sunrisers Hyderabad", "Played": 19, "Won": 9, "Lost": 10},
        {"Opponent": "Punjab Kings", "Played": 27, "Won": 16, "Lost": 11},
        {"Opponent": "Gujarat Titans", "Played": 5, "Won": 1, "Lost": 4},
        {"Opponent": "Lucknow Super Giants", "Played": 4, "Won": 3, "Lost": 1}
    ],
    "Sunrisers Hyderabad": [
        {"Opponent": "Chennai Super Kings", "Played": 20, "Won": 5, "Lost": 15},
        {"Opponent": "Mumbai Indians", "Played": 22, "Won": 9, "Lost": 13},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 23, "Won": 12, "Lost": 11},
        {"Opponent": "Kolkata Knight Riders", "Played": 27, "Won": 9, "Lost": 18},
        {"Opponent": "Delhi Capitals", "Played": 23, "Won": 12, "Lost": 11},
        {"Opponent": "Rajasthan Royals", "Played": 19, "Won": 10, "Lost": 9},
        {"Opponent": "Punjab Kings", "Played": 22, "Won": 15, "Lost": 7},
        {"Opponent": "Gujarat Titans", "Played": 4, "Won": 1, "Lost": 3},
        {"Opponent": "Lucknow Super Giants", "Played": 3, "Won": 1, "Lost": 2}
    ],
    "Lucknow Super Giants": [
        {"Opponent": "Chennai Super Kings", "Played": 5, "Won": 3, "Lost": 2},
        {"Opponent": "Mumbai Indians", "Played": 5, "Won": 4, "Lost": 1},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 4, "Won": 1, "Lost": 3},
        {"Opponent": "Kolkata Knight Riders", "Played": 4, "Won": 3, "Lost": 1},
        {"Opponent": "Delhi Capitals", "Played": 4, "Won": 3, "Lost": 1},
        {"Opponent": "Rajasthan Royals", "Played": 4, "Won": 1, "Lost": 3},
        {"Opponent": "Sunrisers Hyderabad", "Played": 3, "Won": 2, "Lost": 1},
        {"Opponent": "Punjab Kings", "Played": 4, "Won": 3, "Lost": 1},
        {"Opponent": "Gujarat Titans", "Played": 5, "Won": 1, "Lost": 4}
    ],
    "Gujarat Titans": [
        {"Opponent": "Chennai Super Kings", "Played": 6, "Won": 3, "Lost": 3},
        {"Opponent": "Mumbai Indians", "Played": 5, "Won": 3, "Lost": 2},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 4, "Won": 2, "Lost": 2},
        {"Opponent": "Kolkata Knight Riders", "Played": 3, "Won": 2, "Lost": 1},
        {"Opponent": "Delhi Capitals", "Played": 4, "Won": 2, "Lost": 2},
        {"Opponent": "Rajasthan Royals", "Played": 5, "Won": 4, "Lost": 1},
        {"Opponent": "Sunrisers Hyderabad", "Played": 4, "Won": 3, "Lost": 1},
        {"Opponent": "Punjab Kings", "Played": 4, "Won": 2, "Lost": 2},
        {"Opponent": "Lucknow Super Giants", "Played": 5, "Won": 4, "Lost": 1}
    ],
    "Punjab Kings": [
        {"Opponent": "Chennai Super Kings", "Played": 29, "Won": 13, "Lost": 16},
        {"Opponent": "Mumbai Indians", "Played": 31, "Won": 15, "Lost": 16},
        {"Opponent": "Royal Challengers Bengaluru", "Played": 31, "Won": 16, "Lost": 15},
        {"Opponent": "Kolkata Knight Riders", "Played": 32, "Won": 11, "Lost": 21},
        {"Opponent": "Delhi Capitals", "Played": 32, "Won": 16, "Lost": 16},
        {"Opponent": "Rajasthan Royals", "Played": 27, "Won": 11, "Lost": 16},
        {"Opponent": "Sunrisers Hyderabad", "Played": 22, "Won": 7, "Lost": 15},
        {"Opponent": "Gujarat Titans", "Played": 4, "Won": 2, "Lost": 2},
        {"Opponent": "Lucknow Super Giants", "Played": 4, "Won": 1, "Lost": 3}
    ]
}

# Superstar Player Database
PLAYER_DATABASE = {
    "MS Dhoni": {"Total Runs": 5082, "Balls": 3739, "SR": 135.92, "4s": 349, "6s": 239, "HS": 84, "Span": "2008-2024"},
    "V Kohli": {"Total Runs": 8004, "Balls": 6092, "SR": 131.38, "4s": 705, "6s": 272, "HS": 113, "Span": "2008-2024"},
    "RG Sharma": {"Total Runs": 6628, "Balls": 5055, "SR": 131.11, "4s": 599, "6s": 280, "HS": 109, "Span": "2008-2024"},
    "DA Warner": {"Total Runs": 6565, "Balls": 4697, "SR": 139.77, "4s": 663, "6s": 236, "HS": 126, "Span": "2009-2024"},
    "S Dhawan": {"Total Runs": 6769, "Balls": 5326, "SR": 127.14, "4s": 768, "6s": 152, "HS": 106, "Span": "2008-2024"},
    "AB de Villiers": {"Total Runs": 5162, "Balls": 3403, "SR": 151.69, "4s": 413, "6s": 251, "HS": 133, "Span": "2008-2021"},
    "SK Raina": {"Total Runs": 5528, "Balls": 4043, "SR": 136.73, "4s": 506, "6s": 203, "HS": 100, "Span": "2008-2021"},
    "CH Gayle": {"Total Runs": 4965, "Balls": 3333, "SR": 148.96, "4s": 405, "6s": 357, "HS": 175, "Span": "2009-2021"},
    "KL Rahul": {"Total Runs": 4683, "Balls": 3479, "SR": 134.61, "4s": 401, "6s": 187, "HS": 132, "Span": "2013-2024"},
    "AD Russell": {"Total Runs": 2484, "Balls": 1420, "SR": 174.93, "4s": 169, "6s": 209, "HS": 88, "Span": "2012-2024"},
    "RR Pant": {"Total Runs": 3284, "Balls": 2217, "SR": 148.13, "4s": 295, "6s": 154, "HS": 128, "Span": "2016-2024"},
    "Shubman Gill": {"Total Runs": 3216, "Balls": 2370, "SR": 135.70, "4s": 313, "6s": 95, "HS": 129, "Span": "2018-2024"}
}

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Official Team Standings (2008-2026)",
    "⚔️ Head-to-Head (Team vs Team)",
    "👥 Player Comparison",
    "🔥 All-Time Leaders"
])

# TAB 1: STANDINGS
with tab1:
    st.subheader("Official All-Time IPL Team Standings (2008 – 2026)")
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown("#### 🏏 All-Time Franchise Leaderboard")
        for t in TEAMS_DATA:
            badge_class = "rank-badge-1" if t["rank"] == 1 else "rank-badge"
            card_html = f"""
            <div class="team-card" style="border-left: 6px solid {t['color']};">
                <div style="display: flex; align-items: center;">
                    <div class="{badge_class}">{t['rank']}</div>
                    <img src="{t['logo']}" class="team-logo-img" alt="{t['team']}" />
                    <div>
                        <div class="team-name">{t['team']}</div>
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
            
    with col_right:
        st.markdown("#### 📊 All-Time Win Rate Overview")
        df_teams = pd.DataFrame(TEAMS_DATA)
        fig, ax = plt.subplots(figsize=(6, 8.5))
        sns.barplot(data=df_teams, x="rate", y="short", palette="mako", ax=ax)
        ax.set_title("All-Time Win Rate % (2008-2026)", fontsize=12, weight="bold")
        ax.set_xlabel("Win Rate (%)")
        ax.set_ylabel("Franchise")
        ax.set_xlim(0, 80)
        for p in ax.patches:
            val = p.get_width()
            ax.annotate(f"{val:.1f}%", (val + 1, p.get_y() + p.get_height() / 2),
                        ha='left', va='center', fontsize=9, fontweight='bold', color='white')
        st.pyplot(fig)

# TAB 2: HEAD TO HEAD
with tab2:
    st.subheader("⚔️ Head-to-Head: Kis Team Ne Kiske Samne Kitna Jeeta / Haara")
    team_names = [t["team"] for t in TEAMS_DATA]
    selected_team = st.selectbox("Select Team to View Record Against Opponents:", team_names, index=0)
    
    h2h_list = H2H_DATA.get(selected_team, [])
    if h2h_list:
        h2h_df = pd.DataFrame(h2h_list)
        h2h_df["Win %"] = ((h2h_df["Won"] / h2h_df["Played"]) * 100).round(2)
        col_h1, col_h2 = st.columns([1.3, 1.2])
        
        with col_h1:
            st.markdown(f"#### Match Breakdown: **{selected_team}**")
            st.dataframe(h2h_df.set_index("Opponent"), use_container_width=True)
            
        with col_h2:
            st.markdown("#### Wins vs Losses against Each Opponent")
            plot_h2h = h2h_df.melt(id_vars=["Opponent", "Played", "Win %"], value_vars=["Won", "Lost"], var_name="Result", value_name="Matches")
            fig_h2h, ax_h2h = plt.subplots(figsize=(7, 5.5))
            sns.barplot(data=plot_h2h, y="Opponent", x="Matches", hue="Result", palette={"Won": "#10b981", "Lost": "#ef4444"}, ax=ax_h2h)
            ax_h2h.set_title(f"{selected_team} Head-to-Head", fontsize=11, weight="bold")
            st.pyplot(fig_h2h)

# TAB 3: PLAYER COMPARISON
with tab3:
    st.subheader("👥 Compare Two Superstars (2008 – 2026)")
    all_players = sorted(list(PLAYER_DATABASE.keys()))
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("Select Player 1", all_players, index=all_players.index("MS Dhoni"))
    with col2:
        p2 = st.selectbox("Select Player 2", all_players, index=all_players.index("V Kohli"))
        
    s1 = PLAYER_DATABASE[p1]
    s2 = PLAYER_DATABASE[p2]
    comp_df = pd.DataFrame({
        "Metric": ["Span", "Total Runs", "Balls Faced", "Strike Rate", "Fours (4s)", "Sixes (6s)", "Highest Score"],
        p1: [s1["Span"], s1["Total Runs"], s1["Balls"], s1["SR"], s1["4s"], s1["6s"], s1["HS"]],
        p2: [s2["Span"], s2["Total Runs"], s2["Balls"], s2["SR"], s2["4s"], s2["6s"], s2["HS"]]
    }).set_index("Metric")
    st.dataframe(comp_df, use_container_width=True)

# TAB 4: ALL-TIME LEADERS
with tab4:
    st.subheader("🔥 IPL All-Time Historical Leaders (2008 – 2026)")
    df_players = pd.DataFrame([{"Player": k, **v} for k, v in PLAYER_DATABASE.items()])
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        top_runs = df_players.sort_values(by="Total Runs", ascending=False).head(8)
        fig_r, ax_r = plt.subplots(figsize=(7, 4.5))
        sns.barplot(data=top_runs, x="Total Runs", y="Player", palette="viridis", ax=ax_r)
        ax_r.set_title("Most Runs in IPL History", fontsize=11, weight="bold")
        st.pyplot(fig_r)
        
    with col_t2:
        top_sr = df_players.sort_values(by="SR", ascending=False).head(8)
        fig_s, ax_s = plt.subplots(figsize=(7, 4.5))
        sns.barplot(data=top_sr, x="SR", y="Player", palette="magma", ax=ax_s)
        ax_s.set_title("Highest Strike Rates in IPL History", fontsize=11, weight="bold")
        st.pyplot(fig_s)