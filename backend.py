import sqlite3
import pandas as pd
import numpy as np

DB_NAME = "ipl_analytics.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        rank INTEGER PRIMARY KEY,
        team TEXT,
        short TEXT,
        logo TEXT,
        played INTEGER,
        wins INTEGER,
        losses INTEGER,
        nr INTEGER,
        rate REAL,
        color TEXT,
        is_winner INTEGER,
        trophies_count TEXT,
        venue TEXT,
        powerplay_rr REAL,
        middle_rr REAL,
        death_rr REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stadium TEXT,
        matches INTEGER,
        bat_1st_win_pct REAL,
        chase_win_pct REAL,
        avg_1st_innings INTEGER,
        highest_chased INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player_name TEXT PRIMARY KEY,
        category TEXT,
        total_runs INTEGER,
        balls INTEGER,
        strike_rate REAL,
        fours INTEGER,
        sixes INTEGER,
        highest_score INTEGER,
        span TEXT,
        wickets INTEGER,
        economy REAL,
        best_bowling TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS finals (
        season INTEGER PRIMARY KEY,
        winner TEXT,
        defeated TEXT,
        margin TEXT,
        venue TEXT
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM teams;")
    if cursor.fetchone()[0] == 0:
        seed_all_data(cursor)

    conn.commit()
    conn.close()

def seed_all_data(cursor):
    teams_data = [
        (1, "Chennai Super Kings", "CSK", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/5G8eFjkPKNalIgL2FOtovg_500x500.png", 239, 138, 98, 3, 58.47, "#facc15", 1, "5 Titles (2010, '11, '18, '21, '23)", "MA Chidambaram Stadium, Chennai", 8.14, 7.95, 10.92),
        (2, "Mumbai Indians", "MI", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HmiWb77BmJDs6sHvn77v_Q_500x500.png", 261, 144, 113, 4, 56.03, "#0284c7", 1, "5 Titles (2013, '15, '17, '19, '20)", "Wankhede Stadium, Mumbai", 8.28, 8.12, 11.15),
        (3, "Kolkata Knight Riders", "KKR", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/bV4wF2dFs6IPc2BMtjgGZw_500x500.png", 252, 130, 117, 5, 52.63, "#7c3aed", 1, "3 Titles (2012, '14, '24)", "Eden Gardens, Kolkata", 8.52, 8.04, 10.85),
        (4, "Gujarat Titans", "GT", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/aTE8G7q-OcAobWvDd6sizQ_500x500.png", 45, 28, 17, 0, 62.22, "#1e293b", 1, "1 Title (2022)", "Narendra Modi Stadium, Ahmedabad", 8.42, 8.35, 11.20),
        (5, "Lucknow Super Giants", "LSG", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/OqrL0ztLy13FBpvuF6GCBQ_500x500.png", 44, 24, 19, 1, 55.81, "#06b6d4", 0, "Playoffs ('22, '23)", "Ekana Stadium, Lucknow", 8.10, 7.82, 10.45),
        (6, "Rajasthan Royals", "RR", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/GqIU6xhQAnCpy_Cbr2LZRA_500x500.png", 222, 110, 106, 6, 50.93, "#ec4899", 1, "1 Title (2008)", "Sawai Mansingh Stadium, Jaipur", 8.25, 7.98, 10.60),
        (7, "Royal Challengers Bengaluru", "RCB", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/xUS54-BA0dFZPMtbCiHkzQ_500x500.png", 256, 121, 128, 7, 48.59, "#ef4444", 0, "Finalists ('09, '11, '16)", "M. Chinnaswamy Stadium, Bengaluru", 8.45, 8.20, 11.40),
        (8, "Sunrisers Hyderabad", "SRH", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/W0OCBYc05c5MFMrctF62kg_500x500.png", 182, 87, 91, 4, 48.88, "#f97316", 1, "1 Title (2016) | DC '09", "Rajiv Gandhi Stadium, Hyderabad", 8.70, 8.15, 11.05),
        (9, "Delhi Capitals", "DC", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/HzUX6_c8j7pwBCetmct2FQ_500x500.png", 252, 112, 134, 6, 45.53, "#3b82f6", 0, "Finalists ('20)", "Arun Jaitley Stadium, Delhi", 8.32, 7.90, 10.55),
        (10, "Punjab Kings", "PBKS", "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/XUAb4iA3XozYbH_cXQCryQ_500x500.png", 246, 109, 133, 4, 45.04, "#dc2626", 0, "Finalists ('14)", "PCA New Stadium, Mullanpur", 8.30, 7.92, 10.70)
    ]
    cursor.executemany("INSERT INTO teams VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", teams_data)

    venues_data = [
        ("Wankhede Stadium, Mumbai", 116, 46.5, 53.5, 169, 214),
        ("M. Chinnaswamy Stadium, Bengaluru", 94, 43.6, 56.4, 172, 213),
        ("MA Chidambaram Stadium, Chennai", 85, 57.6, 42.4, 164, 208),
        ("Eden Gardens, Kolkata", 93, 42.0, 58.0, 166, 262),
        ("Narendra Modi Stadium, Ahmedabad", 36, 47.2, 52.8, 174, 207),
        ("Rajiv Gandhi Stadium, Hyderabad", 77, 44.1, 55.9, 162, 215),
        ("Arun Jaitley Stadium, Delhi", 89, 45.0, 55.0, 165, 219),
        ("Sawai Mansingh Stadium, Jaipur", 57, 36.8, 63.2, 160, 217)
    ]
    cursor.executemany("INSERT INTO venues (stadium, matches, bat_1st_win_pct, chase_win_pct, avg_1st_innings, highest_chased) VALUES (?,?,?,?,?,?)", venues_data)

    players_data = [
        ("Virat Kohli", "Batter", 8004, 6092, 131.38, 705, 272, 113, "2008-2024", 4, 8.80, "2/25"),
        ("MS Dhoni", "Batter", 5082, 3739, 135.92, 349, 239, 84, "2008-2024", 0, 0.0, "None"),
        ("Rohit Sharma", "Batter", 6628, 5055, 131.11, 599, 280, 109, "2008-2024", 15, 8.02, "4/6"),
        ("AB de Villiers", "Batter", 5162, 3403, 151.69, 413, 251, 133, "2008-2021", 0, 0.0, "None"),
        ("David Warner", "Batter", 6565, 4697, 139.77, 663, 236, 126, "2009-2024", 0, 0.0, "None"),
        ("Shikhar Dhawan", "Batter", 6769, 5326, 127.14, 768, 152, 106, "2008-2024", 4, 8.25, "1/7"),
        ("Suresh Raina", "Batter", 5528, 4043, 136.73, 506, 203, 100, "2008-2021", 25, 7.39, "2/0"),
        ("Chris Gayle", "Batter", 4965, 3333, 148.96, 405, 357, 175, "2009-2021", 18, 7.89, "3/21"),
        ("KL Rahul", "Batter", 4683, 3479, 134.61, 401, 187, 132, "2013-2024", 0, 0.0, "None"),
        ("Andre Russell", "All-Rounder", 2484, 1420, 174.93, 169, 209, 88, "2012-2024", 115, 9.25, "5/15"),
        ("Rishabh Pant", "Batter", 3284, 2217, 148.13, 295, 154, 128, "2016-2024", 0, 0.0, "None"),
        ("Suryakumar Yadav", "Batter", 3594, 2473, 145.33, 381, 130, 103, "2012-2024", 0, 0.0, "None"),
        ("Sanju Samson", "Batter", 4419, 3181, 138.92, 359, 206, 119, "2013-2024", 0, 0.0, "None"),
        ("Shubman Gill", "Batter", 3216, 2370, 135.70, 313, 95, 129, "2018-2024", 0, 0.0, "None"),
        ("Hardik Pandya", "All-Rounder", 2525, 1731, 145.87, 187, 139, 91, "2015-2024", 64, 9.10, "3/17"),
        ("Jos Buttler", "Batter", 3582, 2429, 147.47, 359, 165, 124, "2016-2024", 0, 0.0, "None"),
        ("Yuzvendra Chahal", "Bowler", 37, 85, 43.53, 1, 0, 8, "2013-2024", 205, 7.66, "5/40"),
        ("Jasprit Bumrah", "Bowler", 69, 114, 60.52, 6, 1, 16, "2013-2024", 165, 7.30, "5/10"),
        ("Bhuvneshwar Kumar", "Bowler", 298, 308, 96.75, 23, 4, 24, "2011-2024", 181, 7.56, "5/19"),
        ("Sunil Narine", "All-Rounder", 1534, 921, 166.56, 151, 91, 109, "2012-2024", 180, 6.73, "5/19")
    ]
    cursor.executemany("INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", players_data)

    finals_data = [
        (2024, "Kolkata Knight Riders 🏆", "Sunrisers Hyderabad", "8 wickets", "Chennai"),
        (2023, "Chennai Super Kings 🏆", "Gujarat Titans", "5 wickets (DLS)", "Ahmedabad"),
        (2022, "Gujarat Titans 🏆", "Rajasthan Royals", "7 wickets", "Ahmedabad"),
        (2021, "Chennai Super Kings 🏆", "Kolkata Knight Riders", "27 runs", "Dubai"),
        (2020, "Mumbai Indians 🏆", "Delhi Capitals", "5 wickets", "Dubai"),
        (2019, "Mumbai Indians 🏆", "Chennai Super Kings", "1 run", "Hyderabad"),
        (2018, "Chennai Super Kings 🏆", "Sunrisers Hyderabad", "8 wickets", "Mumbai"),
        (2017, "Mumbai Indians 🏆", "Rising Pune Supergiant", "1 run", "Hyderabad"),
        (2016, "Sunrisers Hyderabad 🏆", "Royal Challengers Bangalore", "8 runs", "Bengaluru"),
        (2015, "Mumbai Indians 🏆", "Chennai Super Kings", "41 runs", "Kolkata"),
        (2014, "Kolkata Knight Riders 🏆", "Kings XI Punjab", "3 wickets", "Bengaluru"),
        (2013, "Mumbai Indians 🏆", "Chennai Super Kings", "23 runs", "Kolkata"),
        (2012, "Kolkata Knight Riders 🏆", "Chennai Super Kings", "5 wickets", "Chennai"),
        (2011, "Chennai Super Kings 🏆", "Royal Challengers Bangalore", "58 runs", "Chennai"),
        (2010, "Chennai Super Kings 🏆", "Mumbai Indians", "22 runs", "Mumbai"),
        (2009, "Deccan Chargers 🏆", "Royal Challengers Bangalore", "6 runs", "Johannesburg"),
        (2008, "Rajasthan Royals 🏆", "Chennai Super Kings", "3 wickets", "Navi Mumbai")
    ]
    cursor.executemany("INSERT INTO finals VALUES (?,?,?,?,?)", finals_data)

def fetch_all_teams():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM teams ORDER BY rank ASC", conn)
    conn.close()
    return df

def fetch_all_venues():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM venues", conn)
    conn.close()
    return df

def fetch_all_players():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()
    return df

def fetch_finals_history():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM finals ORDER BY season DESC", conn)
    conn.close()
    return df

def predict_match_outcome(team1, team2, toss_winner):
    conn = get_connection()
    t1_row = pd.read_sql_query("SELECT rate, powerplay_rr, death_rr FROM teams WHERE team = ?", conn, params=(team1,))
    t2_row = pd.read_sql_query("SELECT rate, powerplay_rr, death_rr FROM teams WHERE team = ?", conn, params=(team2,))
    conn.close()

    if t1_row.empty or t2_row.empty:
        return 50.0, 50.0

    score1 = (t1_row['rate'].values[0] * 0.5) + (t1_row['death_rr'].values[0] * 2.5) + (t1_row['powerplay_rr'].values[0] * 1.5)
    score2 = (t2_row['rate'].values[0] * 0.5) + (t2_row['death_rr'].values[0] * 2.5) + (t2_row['powerplay_rr'].values[0] * 1.5)

    if toss_winner == team1:
        score1 += 3.5
    else:
        score2 += 3.5

    prob1 = round((score1 / (score1 + score2)) * 100, 1)
    prob2 = round(100.0 - prob1, 1)
    return prob1, prob2
