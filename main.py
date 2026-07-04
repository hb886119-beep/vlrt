import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Valorant Damage", layout="wide")

st.title("🔫 발로란트 총 데미지 분석")

# -----------------------
# DB 생성 + 연결
# -----------------------
def get_connection():
    return sqlite3.connect("valorant.db")

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # 테이블 없으면 생성
    cur.execute("""
    CREATE TABLE IF NOT EXISTS guns (
        weapon TEXT,
        range INTEGER,
        damage_head INTEGER,
        damage_body INTEGER,
        damage_leg INTEGER
    )
    """)

    # 데이터가 없으면 샘플 넣기
    cur.execute("SELECT COUNT(*) FROM guns")
    if cur.fetchone()[0] == 0:
        sample_data = [
            ("Vandal", 0, 160, 40, 34),
            ("Vandal", 10, 140, 35, 30),
            ("Vandal", 20, 124, 30, 26),
            ("Phantom", 0, 156, 39, 33),
            ("Phantom", 10, 140, 33, 28),
            ("Phantom", 20, 124, 30, 26),
        ]
        cur.executemany("INSERT INTO guns VALUES (?, ?, ?, ?, ?)", sample_data)

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
# 실행 순서 중요
# -----------------------
init_db()
df = load_data()

# -----------------------
# UI
# -----------------------
weapon = st.sidebar.selectbox("무기 선택", df["weapon"].unique())
filtered = df[df["weapon"] == weapon]

st.dataframe(filtered)

st.line_chart(
    filtered.set_index("range")[["damage_head", "damage_body", "damage_leg"]]
)

st.bar_chart(df.groupby("weapon")[["damage_head", "damage_body", "damage_leg"]].mean())
