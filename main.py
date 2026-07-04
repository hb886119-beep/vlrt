import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Valorant Dashboard", layout="wide")

st.title("🔫 발로란트 무기 분석 대시보드")

# -----------------------
# DB 연결
# -----------------------
def get_connection():
    return sqlite3.connect("valorant.db")

# -----------------------
# DB 초기화
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
        damage_leg INTEGER,
        price INTEGER,
        pick_rate REAL
    )
    """)

    cur.execute("SELECT COUNT(*) FROM guns")
    if cur.fetchone()[0] == 0:

        data = [
            ("Vandal", 0, 160, 40, 34, 2900, 18.5),
            ("Phantom", 0, 156, 39, 33, 2900, 22.1),
            ("Operator", 0, 255, 150, 127, 4700, 12.3),
            ("Sheriff", 0, 160, 55, 47, 800, 10.2),
            ("Ghost", 0, 105, 30, 26, 500, 14.4),

            ("Spectre", 10, 78, 26, 22, 1600, 16.0),
            ("Stinger", 10, 67, 27, 23, 1100, 8.9),
            ("Judge", 10, 34, 17, 14, 1850, 9.1),
            ("Bucky", 10, 40, 20, 17, 850, 7.5),
            ("Marshal", 0, 202, 101, 85, 950, 6.8),

            ("Bulldog", 20, 116, 35, 30, 2050, 11.2),
            ("Guardian", 20, 195, 65, 49, 2250, 5.4),
            ("Ares", 20, 72, 30, 25, 1600, 4.9),
            ("Odin", 20, 95, 38, 32, 3200, 3.8),
            ("Classic", 0, 78, 26, 22, 0, 100.0),

            ("Frenzy", 0, 78, 27, 23, 450, 13.2),
            ("Shorty", 0, 36, 12, 10, 150, 5.1),
            ("Ghost", 20, 88, 25, 22, 500, 14.4),
            ("Vandal", 20, 140, 35, 30, 2900, 18.5),
            ("Phantom", 20, 140, 33, 28, 2900, 22.1),
        ]

        cur.executemany("INSERT INTO guns VALUES (?, ?, ?, ?, ?, ?, ?)", data)

    conn.commit()
    conn.close()

init_db()

st.success("DB 초기화 완료 🚀")
st.write("왼쪽 메뉴에서 Pages 선택하세요")
