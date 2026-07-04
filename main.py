import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Valorant Weapon Analytics", layout="wide")

st.title("🔫 발로란트 무기 데미지 풀 분석")

# -----------------------
# DB 연결
# -----------------------
def get_connection():
    return sqlite3.connect("valorant.db")

# -----------------------
# 풀 데이터 초기화
# -----------------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS guns (
        weapon TEXT,
        range INTEGER,
        damage_head INTEGER,
        damage_body INTEGER,
        damage_leg INTEGER
    )
    """)

    cur.execute("SELECT COUNT(*) FROM guns")
    if cur.fetchone()[0] == 0:

        data = [

            # =====================
            # RIFLES
            # =====================
            ("Vandal", 0, 160, 40, 34),
            ("Vandal", 15, 140, 35, 30),
            ("Vandal", 30, 124, 30, 26),

            ("Phantom", 0, 156, 39, 33),
            ("Phantom", 15, 140, 33, 28),
            ("Phantom", 30, 124, 30, 26),

            ("Guardian", 0, 195, 65, 49),
            ("Guardian", 15, 195, 65, 49),
            ("Guardian", 30, 195, 65, 49),

            ("Bulldog", 0, 116, 35, 30),
            ("Bulldog", 15, 116, 35, 30),
            ("Bulldog", 30, 116, 35, 30),

            # =====================
            # SMG
            # =====================
            ("Spectre", 0, 78, 26, 22),
            ("Spectre", 15, 66, 22, 18),
            ("Spectre", 30, 62, 20, 16),

            ("Stinger", 0, 67, 27, 23),
            ("Stinger", 15, 62, 25, 21),
            ("Stinger", 30, 58, 23, 19),

            # =====================
            # SNIPERS
            # =====================
            ("Operator", 0, 255, 150, 127),
            ("Operator", 50, 255, 150, 127),

            ("Marshal", 0, 202, 101, 85),
            ("Marshal", 50, 202, 101, 85),

            # =====================
            # HEAVY
            # =====================
            ("Ares", 0, 72, 30, 25),
            ("Ares", 20, 67, 28, 24),
            ("Ares", 40, 62, 26, 22),

            ("Odin", 0, 95, 38, 32),
            ("Odin", 20, 85, 35, 30),
            ("Odin", 40, 75, 32, 28),

            # =====================
            # SIDEARMS
            # =====================
            ("Sheriff", 0, 160, 55, 47),
            ("Sheriff", 15, 145, 50, 42),
            ("Sheriff", 30, 145, 50, 42),

            ("Ghost", 0, 105, 30, 26),
            ("Ghost", 15, 88, 25, 22),
            ("Ghost", 30, 78, 22, 19),

            ("Classic", 0, 78, 26, 22),
            ("Classic", 15, 78, 26, 22),
            ("Classic", 30, 78, 26, 22),

            ("Frenzy", 0, 78, 27, 23),
            ("Frenzy", 15, 63, 21, 18),
            ("Frenzy", 30, 63, 21, 18),

            # =====================
            # SHOTGUNS
            # =====================
            ("Judge", 0, 34, 17, 14),
            ("Judge", 10, 20, 10, 8),
            ("Judge", 20, 12, 6, 5),

            ("Bucky", 0, 40, 20, 17),
            ("Bucky", 10, 34, 17, 14),
            ("Bucky", 20, 18, 9, 7),

        ]

        cur.executemany("INSERT INTO guns VALUES (?, ?, ?, ?, ?)", data)

    conn.commit()
    conn.close()

# -----------------------
# 데이터 로드
# -----------------------
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM guns", conn)
    conn.close()
    return df

# -----------------------
# 실행
# -----------------------
init_db()
df = load_data()

# -----------------------
# UI
# -----------------------
weapon = st.sidebar.selectbox("무기 선택", df["weapon"].unique())
filtered = df[df["weapon"] == weapon]

st.subheader(f"📊 {weapon} 데이터")
st.dataframe(filtered)

st.subheader("💥 거리별 데미지")
st.line_chart(
    filtered.set_index("range")[["damage_head", "damage_body", "damage_leg"]]
)

st.subheader("🏆 무기 평균 비교")
st.bar_chart(
    df.groupby("weapon")[["damage_head", "damage_body", "damage_leg"]].mean()
)
