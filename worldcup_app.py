
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# UI
# =========================
st.title("🏆 FIFA World Cup 2026 Simulator - LEVEL 9")
st.subheader("Full Tournament Simulation System")

# =========================
# 上传数据
# =========================
uploaded_file = st.file_uploader(
    "Upload worldcup_data.csv",
    type="csv",
    key="upload_csv"
)

# =========================
# 模型函数
# =========================
def simulate_goals(rate):
    return np.random.poisson(max(rate, 0.1) / 2)

def match(team1, team2, df):

    a1 = df[df["Team"] == team1]["GoalsScored"].values[0]
    d1 = df[df["Team"] == team1]["GoalsConceded"].values[0]

    a2 = df[df["Team"] == team2]["GoalsScored"].values[0]
    d2 = df[df["Team"] == team2]["GoalsConceded"].values[0]

    s1 = a1 - 0.5 * d2
    s2 = a2 - 0.5 * d1

    g1 = simulate_goals(s1)
    g2 = simulate_goals(s2)

    if g1 == g2:
        p1 = df[df["Team"] == team1]["Points"].values[0]
        p2 = df[df["Team"] == team2]["Points"].values[0]
        winner = team1 if p1 >= p2 else team2
    else:
        winner = team1 if g1 > g2 else team2

    return winner, g1, g2


# =========================
# 主程序
# =========================
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### 📊 Teams Data")
    st.dataframe(df)

    # =========================
    # 16队简化（假设输入已经是筛选后的）
    # =========================
    teams = df["Team"].tolist()

    if len(teams) < 8:
        st.warning("Please upload at least 8 teams for tournament simulation.")
        st.stop()

    # =========================
    # Bracket Simulation
    # =========================
    st.write("## ⚔️ Knockout Stage Simulation")

    bracket_log = []

    # QF
    qf_winners = []
    for i in range(0, len(teams), 2):
        w, g1, g2 = match(teams[i], teams[i+1], df)
        qf_winners.append(w)
        bracket_log.append((teams[i], g1, teams[i+1], g2, w))

    # SF
    sf_winners = []
    for i in range(0, len(qf_winners), 2):
        w, g1, g2 = match(qf_winners[i], qf_winners[i+1], df)
        sf_winners.append(w)
        bracket_log.append((qf_winners[i], g1, qf_winners[i+1], g2, w))

    # FINAL
    champion, g1, g2 = match(sf_winners[0], sf_winners[1], df)
    bracket_log.append((sf_winners[0], g1, sf_winners[1], g2, champion))

    # =========================
    # 显示 bracket
    # =========================
    st.write("## 🧭 Tournament Results")

    for m in bracket_log:
        st.write(f"{m[0]} vs {m[2]} → {m[1]}-{m[3]} → Winner: {m[4]}")

    # =========================
    # 冠军
    # =========================
    st.success(f"🏆 Champion: {champion}")

    # =========================
    # Monte Carlo（可选升级）
    # =========================
    if st.button("🎲 Run 1000 Tournament Simulations"):

        results = []

        for _ in range(1000):

            temp_teams = teams.copy()
            np.random.shuffle(temp_teams)

            qf = []
            for i in range(0, len(temp_teams), 2):
                w, _, _ = match(temp_teams[i], temp_teams[i+1], df)
                qf.append(w)

            sf = []
            for i in range(0, len(qf), 2):
                w, _, _ = match(qf[i], qf[i+1], df)
                sf.append(w)

            champ, _, _ = match(sf[0], sf[1], df)
            results.append(champ)

        res = pd.Series(results)

        st.write("### 🏆 Championship Probability (Level 9)")
        st.dataframe(res.value_counts(normalize=True))