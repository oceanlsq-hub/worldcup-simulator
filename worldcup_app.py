import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# UI
# =========================
st.title("🏆 FIFA World Cup 2026 Simulator - LEVEL 9")
st.subheader("Full Tournament Simulation System")

# =========================
# 数据加载 — 默认数据优先，上传备用
# =========================
default_data_path = os.path.join(os.path.dirname(__file__), "data", "worldcup_data.csv")

df = None

if os.path.exists(default_data_path):
    df_default = pd.read_csv(default_data_path)
    st.success(f"✅ 已加载默认数据集（{len(df_default)} 支球队）")
    use_default = st.checkbox("使用默认数据", value=True)
    if use_default:
        df = df_default

if df is None:
    uploaded_file = st.file_uploader("Upload worldcup_data.csv", type="csv", key="upload_csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("请上传 CSV 文件，或勾选上方「使用默认数据」")
        st.stop()

# =========================
# 模型函数
# =========================
def simulate_goals(rate):
    return np.random.poisson(max(rate, 0.1) / 2)


def match(team1, team2, df):
    """
    用 Poisson 模型模拟一场淘汰赛比赛。

    - s1 = team1 均场进球 − 0.5 × team2 均场失球（调整后的期望进攻强度）
    - s2 = team2 均场进球 − 0.5 × team1 均场失球
    - 进球数 ~ Poisson(s / 2)
    - 平局时通过小组赛积分 Points 决定胜者

    注意：0.5 是防守权重系数，简化假设。
    未来可改用 Maher's Model 做更精确的预估。
    """

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

# Build bracket display
col1, col2, col3 = st.columns([1, 1, 1])

# QF matches
with col1:
    st.markdown("**Quarter-Finals**")
    for i, m in enumerate(bracket_log[:4]):
        if m[1] > m[3]:
            label = f"**{m[0]}** {m[1]}-{m[3]} {m[2]}"
        elif m[1] < m[3]:
            label = f"{m[0]} {m[1]}-{m[3]} **{m[2]}**"
        else:
            label = f"{m[0]} {m[1]}-{m[3]} {m[2]} ({m[4]} win)"
        st.write(f"{i+1}. {label}")

# SF matches
with col2:
    st.markdown("**Semi-Finals**")
    for i, m in enumerate(bracket_log[4:6]):
        if m[1] > m[3]:
            label = f"**{m[0]}** {m[1]}-{m[3]} {m[2]}"
        elif m[1] < m[3]:
            label = f"{m[0]} {m[1]}-{m[3]} **{m[2]}**"
        else:
            label = f"{m[0]} {m[1]}-{m[3]} {m[2]} ({m[4]} win)"
        st.write(f"{i+1}. {label}")

# Final
with col3:
    st.markdown("**Final**")
    m = bracket_log[6]
    if m[1] > m[3]:
        label = f"**{m[0]}** {m[1]}-{m[3]} {m[2]}"
    elif m[1] < m[3]:
        label = f"{m[0]} {m[1]}-{m[3]} **{m[2]}**"
    else:
        label = f"{m[0]} {m[1]}-{m[3]} {m[2]} ({m[4]} win)"
    st.write(label)

# Also show a simplified bracket as a step-by-step
st.markdown("### Bracket Flow")
flow = []
for m in bracket_log[:4]:
    flow.append(f"QF: {m[0]} vs {m[2]} → {m[4]}")
for m in bracket_log[4:6]:
    flow.append(f"SF: {m[0]} vs {m[2]} → {m[4]}")
flow.append(f"Final: {m[0]} vs {m[2]} → {m[4]}")
st.write(" → ".join(flow))

# =========================
# 冠军
# =========================
st.success(f"🏆 Champion: {champion}")

# =========================
# Monte Carlo
# =========================
if st.button("🎲 Run 1000 Tournament Simulations"):

    np.random.seed(42)
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

    prob = res.value_counts(normalize=True).reset_index()
    prob.columns = ["Team", "Probability"]
    prob["Probability"] = prob["Probability"].round(3)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = plt.cm.Set2(np.linspace(0, 1, len(prob)))
        bars = ax.barh(prob["Team"], prob["Probability"], color=colors)
        ax.set_xlabel("Championship Probability")
        ax.set_xlim(0, max(prob["Probability"]) * 1.2)
        for bar, p in zip(bars, prob["Probability"]):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                    f"{p:.1%}", va="center", fontsize=10)
        ax.invert_yaxis()
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.dataframe(prob)

    st.caption("点击「重新模拟」可获取新结果")
