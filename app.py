import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="IPL Official Analytics Hub (2008-2026)",
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
        filter: drop-shadow(0px 1px 3px rgba(245, 158, 11, 0.8));
    }
    .trophy-text {
        color: #fcd34d;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.3px;
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

st.markdown(f'<div class="header-container"><img src="{IPL_LOGO_URL}" class="ipl-header-logo" alt="IPL Logo" /><div class="header-text"><h1>Indian Premier League Official Analytics Hub (2008 – 2026)</h1><p>Franchise standings, phase run-rates, stadium analytics, head-to-head records, and match predictor.</p></div></div>', unsafe_allow_html=True)

# 10 Official Teams Data with Home Venues
TEAMS_DATA = [
    {
        "rank": 1, "team": "Chennai Super Kings", "short": "CSK",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/5G8eFjkPKNalIgL2FOtovg_500x500.png",
        "played": 239, "wins": 138, "losses": 98, "nr": 3, "rate": 58.47, "color": "#facc15",
        "is_winner": True, "trophies_count": "5 Titles (2010, '11, '18, '21, '23)",
        "venue": "MA Chidambaram Stadium, Chennai", "powerplay_rr": 8.14, "middle_rr": 7.95, "death_rr": 10.92
    },
    {
        "rank": 2, "team": "Mumbai Indians", "short": "MI",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HmiWb77BmJDs6sHvn77v_Q_500x500.png",
        "played": 261, "wins": 144, "losses": 113, "nr": 4, "rate": 56.03, "color": "#0284c7",
        "is_winner": True, "trophies_count": "5 Titles (2013, '15, '17, '19, '20)",
        "venue": "Wankhede Stadium, Mumbai", "powerplay_rr": 8.28, "middle_rr": 8.12, "death_rr": 11.15
    },
    {
        "rank": 3, "team": "Kolkata Knight Riders", "short": "KKR",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/bV4wF2dFs6IPc2BMtjgGZw_500x500.png",
        "played": 252, "wins": 130, "losses": 117, "nr": 5, "rate": 52.63, "color": "#7c3aed",
        "is_winner": True, "trophies_count": "3 Titles (2012, '14, '24)",
        "venue": "Eden Gardens, Kolkata", "powerplay_rr": 8.52, "middle_rr": 8.04, "death_rr": 10.85
    },
    {
        "rank": 4, "team": "Gujarat Titans", "short": "GT",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/aTE8G7q-OcAobWvDd6sizQ_500x500.png",
        "played": 45, "wins": 28, "losses": 17, "nr": 0, "rate": 62.22, "color": "#1e293b",
        "is_winner": True, "trophies_count": "1 Title (2022)",
        "venue": "Narendra Modi Stadium, Ahmedabad", "powerplay_rr": 8.42, "middle_rr": 8.35, "death_rr": 11.20
    },
    {
        "rank": 5, "team": "Lucknow Super Giants", "short": "LSG",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/OqrL0ztLy13FBpvuF6GCBQ_500x500.png",
        "played": 44, "wins": 24, "losses": 19, "nr": 1, "rate": 55.81, "color": "#06b6d4",
        "is_winner": False, "trophies_count": "Playoffs ('22, '23)",
        "venue": "Ekana Stadium, Lucknow", "powerplay_rr": 8.10, "middle_rr": 7.82, "death_rr": 10.45
    },
    {
        "rank": 6, "team": "Rajasthan Royals", "short": "RR",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/GqIU6xhQAnCpy_Cbr2LZRA_500x500.png",
        "played": 222, "wins": 110, "losses": 106, "nr": 6, "rate": 50.93, "color": "#ec4899",
        "is_winner": True, "trophies_count": "1 Title (2008)",
        "venue": "Sawai Mansingh Stadium, Jaipur", "powerplay_rr": 8.25, "middle_rr": 7.98, "death_rr": 10.60
    },
    {
        "rank": 7, "team": "Royal Challengers Bengaluru", "short": "RCB",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/xUS54-BA0dFZPMtbCiHkzQ_500x500.png",
        "played": 256, "wins": 121, "losses": 128, "nr": 7, "rate": 48.59, "color": "#ef4444",
        "is_winner": False, "trophies_count": "Finalists ('09, '11, '16)",
        "venue": "M. Chinnaswamy Stadium, Bengaluru", "powerplay_rr": 8.45, "middle_rr": 8.20, "death_rr": 11.40
    },
    {
        "rank": 8, "team": "Sunrisers Hyderabad", "short": "SRH",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/W0OCBYc05c5MFMrctF62kg_500x500.png",
        "played": 182, "wins": 87, "losses": 91, "nr": 4, "rate": 48.88, "color": "#f97316",
        "is_winner": True, "trophies_count": "1 Title (2016) | DC '09",
        "venue": "Rajiv Gandhi Stadium, Hyderabad", "powerplay_rr": 8.70, "middle_rr": 8.15, "death_rr": 11.05
    },
    {
        "rank": 9, "team": "Delhi Capitals", "short": "DC",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HzUX6_c8j7pwBCetmct2FQ_500x500.png",
        "played": 252, "wins": 112, "losses": 134, "nr": 6, "rate": 45.53, "color": "#3b82f6",
        "is_winner": False, "trophies_count": "Finalists ('20)",
        "venue": "Arun Jaitley Stadium, Delhi", "powerplay_rr": 8.32, "middle_rr": 7.90, "death_rr": 10.55
    },
    {
        "rank": 10, "team": "Punjab Kings", "short": "PBKS",
        "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/XUAb4iA3XozYbH_cXQCryQ_500x500.png",
        "played": 246, "wins": 109, "losses": 133, "nr": 4, "rate": 45.04, "color": "#dc2626",
        "is_winner": False, "trophies_count": "Finalists ('14)",
        "venue": "PCA New Stadium, Mullanpur", "powerplay_rr": 8.30, "middle_rr": 7.92, "death_rr": 10.70
    }
]

# Stadium Analytics Database
VENUE_DATA = [
    {"Stadium": "Wankhede Stadium, Mumbai", "Matches": 116, "Bat 1st Win %": 46.5, "Chasing Win %": 53.5, "Avg 1st Innings": 169, "Highest Chased": 214},
    {"Stadium": "M. Chinnaswamy Stadium, Bengaluru", "Matches": 94, "Bat 1st Win %": 43.6, "Chasing Win %": 56.4, "Avg 1st Innings": 172, "Highest Chased": 213},
    {"Stadium": "MA Chidambaram Stadium, Chennai", "Matches": 85, "Bat 1st Win %": 57.6, "Chasing Win %": 42.4, "Avg 1st Innings": 164, "Highest Chased": 208},
    {"Stadium": "Eden Gardens, Kolkata", "Matches": 93, "Bat 1st Win %": 42.0, "Chasing Win %": 58.0, "Avg 1st Innings": 166, "Highest Chased": 262},
    {"Stadium": "Narendra Modi Stadium, Ahmedabad", "Matches": 36, "Bat 1st Win %": 47.2, "Chasing Win %": 52.8, "Avg 1st Innings": 174, "Highest Chased": 207},
    {"Stadium": "Rajiv Gandhi Stadium, Hyderabad", "Matches": 77, "Bat 1st Win %": 44.1, "Chasing Win %": 55.9, "Avg 1st Innings": 162, "Highest Chased": 215},
    {"Stadium": "Arun Jaitley Stadium, Delhi", "Matches": 89, "Bat 1st Win %": 45.0, "Chasing Win %": 55.0, "Avg 1st Innings": 165, "Highest Chased": 219},
    {"Stadium": "Sawai Mansingh Stadium, Jaipur", "Matches": 57, "Bat 1st Win %": 36.8, "Chasing Win %": 63.2, "Avg 1st Innings": 160, "Highest Chased": 217}
]

# Finals History
IPL_FINALS_HISTORY = [
    {"Season": 2024, "Winner": "Kolkata Knight Riders 🏆", "Defeated (Against)": "Sunrisers Hyderabad", "Margin": "8 wickets", "Venue": "Chennai"},
    {"Season": 2023, "Winner": "Chennai Super Kings 🏆", "Defeated (Against)": "Gujarat Titans", "Margin": "5 wickets (DLS)", "Venue": "Ahmedabad"},
    {"Season": 2022, "Winner": "Gujarat Titans 🏆", "Defeated (Against)": "Rajasthan Royals", "Margin": "7 wickets", "Venue": "Ahmedabad"},
    {"Season": 2021, "Winner": "Chennai Super Kings 🏆", "Defeated (Against)": "Kolkata Knight Riders", "Margin": "27 runs", "Venue": "Dubai"},
    {"Season": 2020, "Winner": "Mumbai Indians 🏆", "Defeated (Against)": "Delhi Capitals", "Margin": "5 wickets", "Venue": "Dubai"},
    {"Season": 2019, "Winner": "Mumbai Indians 🏆", "Defeated (Against)": "Chennai Super Kings", "Margin": "1 run", "Venue": "Hyderabad"},
    {"Season": 2018, "Winner": "Chennai Super Kings 🏆", "Defeated (Against)": "Sunrisers Hyderabad", "Margin": "8 wickets", "Venue": "Mumbai"},
    {"Season": 2017, "Winner": "Mumbai Indians 🏆", "Defeated (Against)": "Rising Pune Supergiant", "Margin": "1 run", "Venue": "Hyderabad"},
    {"Season": 2016, "Winner": "Sunrisers Hyderabad 🏆", "Defeated (Against)": "Royal Challengers Bangalore", "Margin": "8 runs", "Venue": "Bengaluru"},
    {"Season": 2015, "Winner": "Mumbai Indians 🏆", "Defeated (Against)": "Chennai Super Kings", "Margin": "41 runs", "Venue": "Kolkata"},
    {"Season": 2014, "Winner": "Kolkata Knight Riders 🏆", "Defeated (Against)": "Kings XI Punjab", "Margin": "3 wickets", "Venue": "Bengaluru"},
    {"Season": 2013, "Winner": "Mumbai Indians 🏆", "Defeated (Against)": "Chennai Super Kings", "Margin": "23 runs", "Venue": "Kolkata"},
    {"Season": 2012, "Winner": "Kolkata Knight Riders 🏆", "Defeated (Against)": "Chennai Super Kings", "Margin": "5 wickets", "Venue": "Chennai"},
    {"Season": 2011, "Winner": "Chennai Super Kings 🏆", "Defeated (Against)": "Royal Challengers Bangalore", "Margin": "58 runs", "Venue": "Chennai"},
    {"Season": 2010, "Winner": "Chennai Super Kings 🏆", "Defeated (Against)": "Mumbai Indians", "Margin": "22 runs", "Venue": "Mumbai"},
    {"Season": 2009, "Winner": "Deccan Chargers 🏆", "Defeated (Against)": "Royal Challengers Bangalore", "Margin": "6 runs", "Venue": "Johannesburg"},
    {"Season": 2008, "Winner": "Rajasthan Royals 🏆", "Defeated (Against)": "Chennai Super Kings", "Margin": "3 wickets", "Venue": "Navi Mumbai"}
]

# Head-to-Head Records
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

# Player Database
PLAYER_DATABASE = {
    "Virat Kohli": {"Total Runs": 8004, "Balls": 6092, "Strike Rate": 131.38, "4s": 705, "6s": 272, "Highest Score": 113, "Span": "2008-2024"},
    "MS Dhoni": {"Total Runs": 5082, "Balls": 3739, "Strike Rate": 135.92, "4s": 349, "6s": 239, "Highest Score": 84, "Span": "2008-2024"},
    "Rohit Sharma": {"Total Runs": 6628, "Balls": 5055, "Strike Rate": 131.11, "4s": 599, "6s": 280, "Highest Score": 109, "Span": "2008-2024"},
    "AB de Villiers": {"Total Runs": 5162, "Balls": 3403, "Strike Rate": 151.69, "4s": 413, "6s": 251, "Highest Score": 133, "Span": "2008-2021"},
    "David Warner": {"Total Runs": 6565, "Balls": 4697, "Strike Rate": 139.77, "4s": 663, "6s": 236, "Highest Score": 126, "Span": "2009-2024"},
    "Shikhar Dhawan": {"Total Runs": 6769, "Balls": 5326, "Strike Rate": 127.14, "4s": 768, "6s": 152, "Highest Score": 106, "Span": "2008-2024"},
    "Suresh Raina": {"Total Runs": 5528, "Balls": 4043, "Strike Rate": 136.73, "4s": 506, "6s": 203, "Highest Score": 100, "Span": "2008-2021"},
    "Chris Gayle": {"Total Runs": 4965, "Balls": 3333, "Strike Rate": 148.96, "4s": 405, "6s": 357, "Highest Score": 175, "Span": "2009-2021"},
    "KL Rahul": {"Total Runs": 4683, "Balls": 3479, "Strike Rate": 134.61, "4s": 401, "6s": 187, "Highest Score": 132, "Span": "2013-2024"},
    "Andre Russell": {"Total Runs": 2484, "Balls": 1420, "Strike Rate": 174.93, "4s": 169, "6s": 209, "Highest Score": 88, "Span": "2012-2024"},
    "Rishabh Pant": {"Total Runs": 3284, "Balls": 2217, "Strike Rate": 148.13, "4s": 295, "6s": 154, "Highest Score": 128, "Span": "2016-2024"},
    "Suryakumar Yadav": {"Total Runs": 3594, "Balls": 2473, "Strike Rate": 145.33, "4s": 381, "6s": 130, "Highest Score": 103, "Span": "2012-2024"},
    "Sanju Samson": {"Total Runs": 4419, "Balls": 3181, "Strike Rate": 138.92, "4s": 359, "6s": 206, "Highest Score": 119, "Span": "2013-2024"},
    "Shubman Gill": {"Total Runs": 3216, "Balls": 2370, "Strike Rate": 135.70, "4s": 313, "6s": 95, "Highest Score": 129, "Span": "2018-2024"},
    "Hardik Pandya": {"Total Runs": 2525, "Balls": 1731, "Strike Rate": 145.87, "4s": 187, "6s": 139, "Highest Score": 91, "Span": "2015-2024"},
    "Jos Buttler": {"Total Runs": 3582, "Balls": 2429, "Strike Rate": 147.47, "4s": 359, "6s": 165, "Highest Score": 124, "Span": "2016-2024"}
}

# Bowlers Data
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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏆 Standings & Trophies",
    "⚡ All Teams Phase Breakdown",
    "🏟️ Stadium Analytics",
    "👥 Player Head-to-Head",
    "⚡ Strike Rate & Run Leaders",
    "🥇 Finals History",
    "⚔️ Team Head-to-Head",
    "🔮 Match Predictor"
])

# ==========================================
# TAB 1: STANDINGS
# ==========================================
with tab1:
    st.subheader("All-Time Standings & Championship Winners (2008 – 2026)")
    col_l, col_r = st.columns([1.65, 1])
    with col_l:
        for t in TEAMS_DATA:
            badge_class = "rank-badge-1" if t["rank"] == 1 else "rank-badge"
            
            if t["is_winner"]:
                trophy_badge_html = f'<span class="trophy-badge-container"><span class="trophy-icon-symbol">🏆</span><span class="trophy-text">{t["trophies_count"]}</span></span>'
            else:
                trophy_badge_html = f'<span style="background: rgba(156, 163, 175, 0.15); border: 1px solid #4b5563; padding: 2px 8px; border-radius: 12px; font-size: 11px; color: #9ca3af; margin-left: 8px;">{t["trophies_count"]}</span>'

            card_html = f'<div class="team-card" style="border-left: 6px solid {t["color"]};"><div style="display: flex; align-items: center;"><div class="{badge_class}">{t["rank"]}</div><img src="{t["logo"]}" class="team-logo-img" alt="{t["team"]}" /><div><div style="display: flex; align-items: center; flex-wrap: wrap;"><span class="team-name">{t["team"]}</span>{trophy_badge_html}</div><div class="matches-subtext">Matches: {t["played"]} | Won: {t["wins"]} | Lost: {t["losses"]} | Home: {t["venue"].split(",")[0]}</div></div></div><div style="text-align: right;"><div class="rate-val">{t["rate"]}%</div><div class="rate-label">Win Rate</div></div></div>'
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
# TAB 2: ALL TEAMS PHASE BREAKDOWN (NEW)
# ==========================================
with tab2:
    st.subheader("⚡ All 10 Teams: Powerplay, Middle & Death Overs Run Rate")
    st.markdown("Analyze how aggressively each franchise scores across different match phases.")
    
    phase_df = pd.DataFrame([
        {
            "Team": t["team"],
            "Short": t["short"],
            "Powerplay (1-6)": t["powerplay_rr"],
            "Middle Overs (7-15)": t["middle_rr"],
            "Death Overs (16-20)": t["death_rr"]
        } for t in TEAMS_DATA
    ])
    
    st.dataframe(phase_df.set_index("Team"), use_container_width=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### 💥 Powerplay Aggression (Run Rate)")
        fig_pp, ax_pp = plt.subplots(figsize=(7, 4.5))
        sns.barplot(data=phase_df.sort_values(by="Powerplay (1-6)", ascending=False), x="Powerplay (1-6)", y="Short", palette="flare", ax=ax_pp)
        ax_pp.set_xlim(7.5, 9.2)
        ax_pp.set_xlabel("Run Rate per Over")
        st.pyplot(fig_pp)
        
    with col_p2:
        st.markdown("#### 🔥 Death Overs Finishing Power (Run Rate)")
        fig_d, ax_d = plt.subplots(figsize=(7, 4.5))
        sns.barplot(data=phase_df.sort_values(by="Death Overs (16-20)", ascending=False), x="Death Overs (16-20)", y="Short", palette="crest", ax=ax_d)
        ax_d.set_xlim(9.5, 12.0)
        ax_d.set_xlabel("Run Rate per Over")
        st.pyplot(fig_d)

# ==========================================
# TAB 3: STADIUM & VENUE ANALYTICS (NEW)
# ==========================================
with tab3:
    st.subheader("🏟️ Stadium Analytics: Batting 1st vs Chasing Win Rates")
    v_df = pd.DataFrame(VENUE_DATA)
    
    st.dataframe(v_df.set_index("Stadium"), use_container_width=True)
    
    sel_venue = st.selectbox("Select Stadium for Deep Insights:", [v["Stadium"] for v in VENUE_DATA])
    target_v = next(item for item in VENUE_DATA if item["Stadium"] == sel_venue)
    
    col_v1, col_v2, col_v3 = st.columns(3)
    col_v1.metric("Total Matches Played", target_v["Matches"])
    col_v2.metric("Chasing Team Win %", f"{target_v['Chasing Win %']}%")
    col_v3.metric("Avg 1st Innings Score", target_v["Avg 1st Innings"])

# ==========================================
# TAB 4: PLAYER HEAD-TO-HEAD COMPARISON
# ==========================================
with tab4:
    st.subheader("👥 Compare Two Superstars (All-Time Stats & Strike Rates)")
    all_players = sorted(list(PLAYER_DATABASE.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("Select Player 1", all_players, index=all_players.index("MS Dhoni"))
    with col2:
        p2 = st.selectbox("Select Player 2", all_players, index=all_players.index("Virat Kohli"))
        
    s1 = PLAYER_DATABASE[p1]
    s2 = PLAYER_DATABASE[p2]
    
    comp_df = pd.DataFrame({
        "Metric": ["Career Span", "Total Runs", "Balls Faced", "Strike Rate", "Fours (4s)", "Sixes (6s)", "Highest Score"],
        p1: [s1["Span"], s1["Total Runs"], s1["Balls"], s1["Strike Rate"], s1["4s"], s1["6s"], s1["Highest Score"]],
        p2: [s2["Span"], s2["Total Runs"], s2["Balls"], s2["Strike Rate"], s2["4s"], s2["6s"], s2["Highest Score"]]
    }).set_index("Metric")
    
    st.dataframe(comp_df, use_container_width=True)
    
    chart_data = pd.DataFrame({
        'Metric': ['Total Runs', 'Strike Rate', 'Fours (4s)', 'Sixes (6s)'],
        p1: [s1['Total Runs'], s1['Strike Rate'], s1['4s'], s1['6s']],
        p2: [s2['Total Runs'], s2['Strike Rate'], s2['4s'], s2['6s']]
    }).melt(id_vars='Metric', var_name='Player', value_name='Value')
    
    fig_comp, ax_comp = plt.subplots(figsize=(9, 4.5))
    sns.barplot(data=chart_data, x='Metric', y='Value', hue='Player', palette="viridis", ax=ax_comp)
    ax_comp.set_title(f"{p1} vs {p2} Comparative Metrics", fontsize=12, weight="bold")
    st.pyplot(fig_comp)

# ==========================================
# TAB 5: STRIKE RATES & RUN LEADERS
# ==========================================
with tab5:
    st.subheader("⚡ All-Time Batsmen Strike Rates & Run Scorer Rankings")
    df_players = pd.DataFrame([{"Player": k, **v} for k, v in PLAYER_DATABASE.items()])
    
    col_lead1, col_lead2 = st.columns(2)
    with col_lead1:
        st.markdown("#### 🏏 Highest Strike Rates")
        top_sr = df_players.sort_values(by="Strike Rate", ascending=False).head(10)
        fig_s, ax_s = plt.subplots(figsize=(7, 5))
        sns.barplot(data=top_sr, x="Strike Rate", y="Player", palette="magma", ax=ax_s)
        ax_s.set_xlim(0, 190)
        for p in ax_s.patches:
            val = p.get_width()
            ax_s.annotate(f"{val:.1f}", (val + 1, p.get_y() + p.get_height() / 2),
                          ha='left', va='center', fontsize=9, fontweight='bold', color='white')
        st.pyplot(fig_s)
        
    with col_lead2:
        st.markdown("#### 🏅 All-Time Highest Run Scorers")
        top_runs = df_players.sort_values(by="Total Runs", ascending=False).head(10)
        fig_r, ax_r = plt.subplots(figsize=(7, 5))
        sns.barplot(data=top_runs, x="Total Runs", y="Player", palette="viridis", ax=ax_r)
        ax_r.set_xlim(0, 9000)
        for p in ax_r.patches:
            val = p.get_width()
            ax_r.annotate(f"{int(val)}", (val + 50, p.get_y() + p.get_height() / 2),
                          ha='left', va='center', fontsize=9, fontweight='bold', color='white')
        st.pyplot(fig_r)

# ==========================================
# TAB 6: FINALS HISTORY
# ==========================================
with tab6:
    st.subheader("🥇 IPL Finals History: Champion Winners (2008 - Present)")
    finals_df = pd.DataFrame(IPL_FINALS_HISTORY)
    st.dataframe(finals_df.set_index("Season"), use_container_width=True)

# ==========================================
# TAB 7: TEAM HEAD TO HEAD
# ==========================================
with tab7:
    st.subheader("Head-to-Head Matrix")
    team_names = [t["team"] for t in TEAMS_DATA]
    sel_team = st.selectbox("Select Team:", team_names, index=0)
    data_list = H2H_DATA.get(sel_team, H2H_DATA["Chennai Super Kings"])
    h_df = pd.DataFrame(data_list)
    h_df["Win %"] = ((h_df["Won"] / h_df["Played"]) * 100).round(2)
    st.dataframe(h_df.set_index("Opponent"), use_container_width=True)

# ==========================================
# TAB 8: MATCH PREDICTOR
# ==========================================
with tab8:
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
