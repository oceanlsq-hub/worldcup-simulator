import pandas as pd

df = pd.read_csv("/Users/linshangqing/Downloads/VScode/WorldCup2026/data/worldcup_data.csv")

print(df.head())
print(df.columns)
print(df.shape)
df["Attack"] = df["GoalsScored"] / 1
df["Defense"] = df["GoalsConceded"] / 1

df["PowerScore"] = (
    df["Points"] * 3
    + df["Attack"] * 2
    - df["Defense"] * 2
)
df_sorted = df.sort_values(by="PowerScore", ascending=False)
print(df_sorted)
print(df_sorted)
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.bar(df_sorted["Team"], df_sorted["PowerScore"])
plt.title("Improved World Cup Power Ranking")
plt.xticks(rotation=45)
plt.show()
df["WinProb"] = df["PowerScore"] / df["PowerScore"].sum()
print(df[["Team", "PowerScore", "WinProb"]])
import numpy as np

winner = np.random.choice(df["Team"], p=df["WinProb"])
print("Simulated Champion:", winner)
results = []

for _ in range(10000):
    winner = np.random.choice(df["Team"], p=df["WinProb"])
    results.append(winner)

result_series = pd.Series(results)
print(result_series.value_counts(normalize=True))
results = []

for _ in range(10000):
    winner = np.random.choice(df["Team"], p=df["WinProb"])
    results.append(winner)

result_series = pd.Series(results)
prob = result_series.value_counts(normalize=True)
plt.figure(figsize=(10,5))
plt.bar(prob.index, prob.values)
plt.title("World Cup 2026 Championship Probability")
plt.xticks(rotation=45)
plt.show()
top5 = df_sorted.head(5)

plt.figure(figsize=(8,5))
plt.bar(top5["Team"], top5["PowerScore"])
plt.title("Top 5 Teams Power Ranking")
plt.xticks(rotation=45)
plt.show()
print("=== WORLD CUP ANALYSIS SUMMARY ===")
print("Top Team:", df_sorted.iloc[0]["Team"])
print("Most Likely Champion:", prob.idxmax())
print("Champion Probability:", prob.max())
import numpy as np
import pandas as pd

# =========================
# STEP 1: 实力值
# =========================
df["Strength"] = df["PowerScore"]

# =========================
# STEP 2: 比赛函数
# =========================
def simulate_match(team1, team2):
    p1 = df[df["Team"] == team1]["Strength"].values[0]
    p2 = df[df["Team"] == team2]["Strength"].values[0]

    prob1 = p1 / (p1 + p2)

    return team1 if np.random.rand() < prob1 else team2


# =========================
# STEP 3-7: 模拟 10000 次世界杯
# =========================
results = []

for _ in range(10000):

    teams = df["Team"].tolist()

    # STEP 4: 四分之一决赛
    qf = []
    for i in range(0, len(teams), 2):
        qf.append(simulate_match(teams[i], teams[i+1]))

    # STEP 5: 半决赛
    sf = []
    for i in range(0, len(qf), 2):
        sf.append(simulate_match(sf[i] if False else qf[i], qf[i+1]))

    # 修复写法（更清晰）
    sf = []
    for i in range(0, len(qf), 2):
        sf.append(simulate_match(qf[i], qf[i+1]))

    # STEP 6: 决赛
    champion = simulate_match(sf[0], sf[1])

    # STEP 7: 记录
    results.append(champion)


# =========================
# 输出结果
# =========================
result_series = pd.Series(results)

print("\n=== CHAMPION PROBABILITIES ===")
print(result_series.value_counts(normalize=True))
import numpy as np

df["Attack"] = df["GoalsScored"]
df["Defense"] = df["GoalsConceded"]
def simulate_goals(attack_strength):
    return np.random.poisson(lam=attack_strength / 2)
def simulate_match(team1, team2):

    t1_attack = df[df["Team"] == team1]["Attack"].values[0]
    t2_attack = df[df["Team"] == team2]["Attack"].values[0]

    t1_goals = simulate_goals(t1_attack)
    t2_goals = simulate_goals(t2_attack)

    if t1_goals > t2_goals:
        return team1
    elif t2_goals > t1_goals:
        return team2
    else:
        # 平局 → 用实力决定（简化点球）
        p1 = df[df["Team"] == team1]["PowerScore"].values[0]
        p2 = df[df["Team"] == team2]["PowerScore"].values[0]
        return team1 if p1 > p2 else team2
    results = []

for _ in range(10000):

    teams = df["Team"].tolist()

    # QF
    qf = []
    for i in range(0, len(teams), 2):
        qf.append(simulate_match(teams[i], teams[i+1]))

    # SF
    sf = []
    for i in range(0, len(qf), 2):
        sf.append(simulate_match(qf[i], qf[i+1]))

    # Final
    champion = simulate_match(sf[0], sf[1])

    results.append(champion)

import pandas as pd

result_series = pd.Series(results)

print("\n=== REALISTIC SIMULATION CHAMPION PROB ===")
print(result_series.value_counts(normalize=True))
import numpy as np
import pandas as pd

# =========================
# STEP 1: 构建球队能力
# =========================
df["Attack"] = df["GoalsScored"]
df["Defense"] = df["GoalsConceded"]

# =========================
# STEP 2: 进球模型（Poisson）
# =========================
def simulate_goals(rate):
    return np.random.poisson(lam=max(rate, 0.1) / 2)

# =========================
# STEP 3: 比赛模拟（更真实版本）
# =========================
def simulate_match(team1, team2):

    t1_attack = df[df["Team"] == team1]["Attack"].values[0]
    t2_attack = df[df["Team"] == team2]["Attack"].values[0]

    t1_def = df[df["Team"] == team1]["Defense"].values[0]
    t2_def = df[df["Team"] == team2]["Defense"].values[0]

    # 核心：攻击 - 对方防守影响
    t1_strength = t1_attack - 0.5 * t2_def
    t2_strength = t2_attack - 0.5 * t1_def

    t1_goals = simulate_goals(t1_strength)
    t2_goals = simulate_goals(t2_strength)

    # 胜负判断
    if t1_goals > t2_goals:
        return team1
    elif t2_goals > t1_goals:
        return team2
    else:
        # 平局 → 用 PowerScore + 随机性
        p1 = df[df["Team"] == team1]["PowerScore"].values[0]
        p2 = df[df["Team"] == team2]["PowerScore"].values[0]

        return team1 if (p1 + np.random.rand()) > (p2 + np.random.rand()) else team2

# =========================
# STEP 4: 10000次世界杯模拟
# =========================
results = []

for _ in range(10000):

    teams = df["Team"].tolist()

    # QF
    qf = []
    for i in range(0, len(teams), 2):
        qf.append(simulate_match(teams[i], teams[i+1]))

    # SF
    sf = []
    for i in range(0, len(qf), 2):
        sf.append(simulate_match(qf[i], qf[i+1]))

    # FINAL
    champion = simulate_match(sf[0], sf[1])

    results.append(champion)

# =========================
# STEP 5: 输出结果
# =========================
result_series = pd.Series(results)

print("\n🏆 LEVEL 4 REALISTIC WORLD CUP SIMULATION")
print(result_series.value_counts(normalize=True))

import numpy as np
import pandas as pd

# =========================
# STEP 1: 基础能力
# =========================
df["Attack"] = df["GoalsScored"]
df["Defense"] = df["GoalsConceded"]

# =========================
# STEP 2: 进球模型
# =========================
def simulate_goals(rate):
    return np.random.poisson(max(rate, 0.1) / 2)

# =========================
# STEP 3: 比赛模拟
# =========================
def simulate_match(team1, team2):

    a1 = df[df["Team"] == team1]["Attack"].values[0]
    d1 = df[df["Team"] == team1]["Defense"].values[0]

    a2 = df[df["Team"] == team2]["Attack"].values[0]
    d2 = df[df["Team"] == team2]["Defense"].values[0]

    s1 = a1 - 0.5 * d2
    s2 = a2 - 0.5 * d1

    g1 = simulate_goals(s1)
    g2 = simulate_goals(s2)

    if g1 > g2:
        return team1
    elif g2 > g1:
        return team2
    else:
        # 平局 → 用 PowerScore + randomness
        p1 = df[df["Team"] == team1]["PowerScore"].values[0]
        p2 = df[df["Team"] == team2]["PowerScore"].values[0]
        return team1 if (p1 + np.random.rand()) > (p2 + np.random.rand()) else team2


# =========================
# STEP 4: 小组赛（简化8队=2组）
# =========================
groups = {
    "A": df["Team"].tolist()[:4],
    "B": df["Team"].tolist()[4:]
}

group_results = {}

for g, teams in groups.items():

    table = {t: {"pts":0, "gd":0} for t in teams}

    # 每队互打
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):

            t1, t2 = teams[i], teams[j]

            a1 = df[df["Team"] == t1]["Attack"].values[0]
            d1 = df[df["Team"] == t1]["Defense"].values[0]

            a2 = df[df["Team"] == t2]["Attack"].values[0]
            d2 = df[df["Team"] == t2]["Defense"].values[0]

            s1 = a1 - 0.5 * d2
            s2 = a2 - 0.5 * d1

            g1 = simulate_goals(s1)
            g2 = simulate_goals(s2)

            # 更新净胜球
            table[t1]["gd"] += (g1 - g2)
            table[t2]["gd"] += (g2 - g1)

            # 积分
            if g1 > g2:
                table[t1]["pts"] += 3
            elif g2 > g1:
                table[t2]["pts"] += 3
            else:
                table[t1]["pts"] += 1
                table[t2]["pts"] += 1

    # 排名（积分+净胜球）
    ranked = sorted(teams, key=lambda x: (table[x]["pts"], table[x]["gd"]), reverse=True)

    group_results[g] = ranked[:2]   # 前2出线

print("\n🏆 GROUP QUALIFIERS:")
print(group_results)


# =========================
# STEP 5: 淘汰赛
# =========================
qualified = group_results["A"] + group_results["B"]

results = []

for _ in range(10000):

    teams = qualified.copy()

    # QF
    qf = []
    for i in range(0, len(teams), 2):
        qf.append(simulate_match(teams[i], teams[i+1]))

    # SF
    sf = []
    for i in range(0, len(qf), 2):
        sf.append(simulate_match(qf[i], qf[i+1]))

    # FINAL
    champ = simulate_match(sf[0], sf[1])

    results.append(champ)


# =========================
# STEP 6: 输出冠军概率
# =========================
result_series = pd.Series(results)

print("\n🏆 FINAL CHAMPION PROBABILITY (LEVEL 5)")
print(result_series.value_counts(normalize=True))

import numpy as np
import pandas as pd

# =========================
# 基础能力
# =========================
df["Attack"] = df["GoalsScored"]
df["Defense"] = df["GoalsConceded"]

def simulate_goals(rate):
    return np.random.poisson(max(rate, 0.1) / 2)

# =========================
# 比赛模拟（返回比分）
# =========================
def simulate_match(team1, team2):

    a1 = df[df["Team"] == team1]["Attack"].values[0]
    d1 = df[df["Team"] == team1]["Defense"].values[0]

    a2 = df[df["Team"] == team2]["Attack"].values[0]
    d2 = df[df["Team"] == team2]["Defense"].values[0]

    s1 = a1 - 0.5 * d2
    s2 = a2 - 0.5 * d1

    g1 = simulate_goals(s1)
    g2 = simulate_goals(s2)

    if g1 > g2:
        return team1, team2, g1, g2
    elif g2 > g1:
        return team1, team2, g1, g2
    else:
        p1 = df[df["Team"] == team1]["PowerScore"].values[0]
        p2 = df[df["Team"] == team2]["PowerScore"].values[0]

        winner = team1 if (p1 + np.random.rand()) > (p2 + np.random.rand()) else team2

        if winner == team1:
            return team1, team2, g1+1, g2
        else:
            return team1, team2, g1, g2+1


# =========================
# 小组赛（简化）
# =========================
groups = {
    "A": df["Team"].tolist()[:4],
    "B": df["Team"].tolist()[4:]
}

group_results = {}

print("\n🏟 GROUP STAGE RESULTS")

for g, teams in groups.items():

    table = {t: {"pts":0, "gd":0} for t in teams}

    for i in range(len(teams)):
        for j in range(i+1, len(teams)):

            t1, t2, g1, g2 = simulate_match(teams[i], teams[j])

            table[t1]["gd"] += (g1 - g2)
            table[t2]["gd"] += (g2 - g1)

            if g1 > g2:
                table[t1]["pts"] += 3
            elif g2 > g1:
                table[t2]["pts"] += 3
            else:
                table[t1]["pts"] += 1
                table[t2]["pts"] += 1

            print(f"{t1} {g1} - {g2} {t2}")

    ranked = sorted(teams, key=lambda x: (table[x]["pts"], table[x]["gd"]), reverse=True)

    group_results[g] = ranked[:2]

print("\n🏆 QUALIFIED TEAMS:")
print(group_results)


# =========================
# 淘汰赛 + bracket记录
# =========================
qualified = group_results["A"] + group_results["B"]

bracket = []

print("\n⚔️ KNOCKOUT STAGE")

for i in range(1000):

    teams = qualified.copy()
    matches = []

    # QF
    qf = []
    for j in range(0, len(teams), 2):
        t1, t2, g1, g2 = simulate_match(teams[j], teams[j+1])
        winner = t1 if g1 > g2 else t2
        qf.append(winner)
        matches.append((t1, g1, t2, g2))

    # SF
    sf = []
    for j in range(0, len(qf), 2):
        t1, t2, g1, g2 = simulate_match(qf[j], qf[j+1])
        winner = t1 if g1 > g2 else t2
        sf.append(winner)
        matches.append((t1, g1, t2, g2))

    # FINAL
    t1, t2, g1, g2 = simulate_match(sf[0], sf[1])
    champion = t1 if g1 > g2 else t2

    matches.append((t1, g1, t2, g2))

    bracket.append(champion)

# =========================
# 输出冠军概率
# =========================
result_series = pd.Series(bracket)

print("\n🏆 FINAL WORLD CUP WINNER PROBABILITY (LEVEL 6)")
print(result_series.value_counts(normalize=True))