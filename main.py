import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# -----------------------
# DB 연결 (SQLite 기준)
# -----------------------
def get_connection():
    return sqlite3.connect("valorant.db")

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
# UI 설정
# -----------------------
st.set_page_config(page_title="Valorant Gun Damage", layout="wide")

st.title("🔫 발로란트 총 데미지 분석")

df = load_data()

# -----------------------
# 사이드 필터
# -----------------------
st.sidebar.header("필터")

weapon_list = df["weapon"].unique()
selected_weapon = st.sidebar.selectbox("무기 선택", weapon_list)

filtered_df = df[df["weapon"] == selected_weapon]

# -----------------------
# 데이터 보기
# -----------------------
st.subheader("📊 데이터 테이블")
st.dataframe(filtered_df)

# -----------------------
# 데미지 시각화
# -----------------------
st.subheader("💥 거리별 데미지")

fig, ax = plt.subplots()

ax.plot(filtered_df["range"], filtered_df["damage_head"], label="Head")
ax.plot(filtered_df["range"], filtered_df["damage_body"], label="Body")
ax.plot(filtered_df["range"], filtered_df["damage_leg"], label="Leg")

ax.set_xlabel("Distance")
ax.set_ylabel("Damage")
ax.set_title(f"{selected_weapon} Damage Drop-off")
ax.legend()

st.pyplot(fig)

# -----------------------
# 전체 비교 (옵션)
# -----------------------
st.subheader("🔥 무기별 평균 데미지 비교")

avg_df = df.groupby("weapon")[["damage_head", "damage_body", "damage_leg"]].mean()

st.bar_chart(avg_df)
