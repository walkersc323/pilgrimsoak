import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pilgrim's Oak Round", layout="centered")

# 1. Smaller Page Title
st.markdown("### ⛳ Pilgrim's Oak Round")
st.caption("White / Gold Tees • Par 72 • 5,828 Yards")

# --- MATCH SETUP (COLLAPSIBLE / TOP BAR) ---
with st.expander("⚙️ Player Setup & Handicaps", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.text_input("Player 1 Name", value="ATN")
        p1_hcp = st.number_input(f"{p1} Handicap", value=12, min_value=0, max_value=36, step=1)
    with col2:
        p2 = st.text_input("Player 2 Name", value="Player 2")
        p2_hcp = st.number_input(f"{p2} Handicap", value=0, min_value=0, max_value=36, step=1)

# --- COURSE DATA ---
COURSE_DATA = {
    "Hole": list(range(1, 19)),
    "Yards": [378, 327, 367, 108, 329, 470, 354, 138, 425, 350, 359, 101, 329, 505, 360, 352, 111, 465],
    "Par": [4, 4, 4, 3, 4, 5, 4, 3, 5, 4, 4, 3, 4, 5, 4, 4, 3, 5],
    "Hcp": [11, 5, 9, 17, 15, 13, 3, 7, 1, 16, 4, 6, 8, 12, 10, 18, 14, 2]
}

if "score_data" not in st.session_state:
    df_init = pd.DataFrame(COURSE_DATA)
    df_init[p1] = 0
    df_init[p2] = 0
    st.session_state.score_data = df_init

df = st.session_state.score_data
if p1 not in df.columns or p2 not in df.columns:
    df.columns = ["Hole", "Yards", "Par", "Hcp", p1, p2]

# --- CALCULATE POINTS ---
p1_pts = 0
p2_pts = 0

for _, row in df.iterrows():
    h_hcp = int(row["Hcp"])
    g1 = int(row[p1])
    g2 = int(row[p2])

    p1_strokes = 1 if h_hcp <= p1_hcp else 0
    p2_strokes = 1 if h_hcp <= p2_hcp else 0

    net1 = g1 - p1_strokes if g1 > 0 else 0
    net2 = g2 - p2_strokes if g2 > 0 else 0

    if h_hcp <= 6:
        hole_val = 9
    elif h_hcp <= 12:
        hole_val = 6
    else:
        hole_val = 3

    if g1 > 0 and g2 > 0:
        if net1 < net2:
            p1_pts += hole_val
        elif net2 < net1:
            p2_pts += hole_val
        else:
            p1_pts += hole_val // 2
            p2_pts += hole_val // 2

# 2. Points Leaderboard Just Under Title (In Boxes, No Gross Strokes)
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f"""
        <div style="border: 2px solid #31333F; border-radius: 8px; padding: 12px; text-align: center; background-color: #F0F2F6;">
            <span style="font-size: 14px; color: #555; font-weight: bold;">{p1}</span><br>
            <span style="font-size: 28px; font-weight: bold; color: #1E1E1E;">{int(p1_pts)} PTS</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"""
        <div style="border: 2px solid #31333F; border-radius: 8px; padding: 12px; text-align: center; background-color: #F0F2F6;">
            <span style="font-size: 14px; color: #555; font-weight: bold;">{p2}</span><br>
            <span style="font-size: 28px; font-weight: bold; color: #1E1E1E;">{int(p2_pts)} PTS</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# 5. Hole Selector for Quick On-Course Entry
selected_hole = st.number_input("Select Hole Being Played", min_value=1, max_value=18, step=1, value=1)
hole_info = df[df["Hole"] == selected_hole].iloc[0]

hole_hcp = int(hole_info["Hcp"])
hole_par = int(hole_info["Par"])
hole_yards = int(hole_info["Yards"])

# 4. Mark in RED when ATN gets a stroke on the hole
atn_gets_stroke = hole_hcp <= p1_hcp
stroke_badge = "🔴 <span style='color: red; font-weight: bold;'>(ATN GETS A STROKE)</span>" if atn_gets_stroke else ""

# 3. Hole Details Header (Hole Number, Yardage, Handicap, Par)
st.markdown(
    f"#### Hole {selected_hole} &nbsp;|&nbsp; {hole_yards} Yds &nbsp;|&nbsp; Par {hole_par} &nbsp;|&nbsp; Hcp {hole_hcp} {stroke_badge}",
    unsafe_allow_html=True
)

# Hole Point Value
val_text = "9 PTS" if hole_hcp <= 6 else "6 PTS" if hole_hcp <= 12 else "3 PTS"
st.caption(f"Walker Cup Value: **{val_text}**")

# Score Entry Inputs for Current Hole
e1, e2 = st.columns(2)
with e1:
    curr_p1_score = int(df.loc[df["Hole"] == selected_hole, p1].values[0])
    new_p1 = st.number_input(f"{p1} Score", min_value=0, max_value=15, value=curr_p1_score, key=f"p1_h{selected_hole}")
with e2:
    curr_p2_score = int(df.loc[df["Hole"] == selected_hole, p2].values[0])
    new_p2 = st.number_input(f"{p2} Score", min_value=0, max_value=15, value=curr_p2_score, key=f"p2_h{selected_hole}")

# Update state on edit
if new_p1 != curr_p1_score or new_p2 != curr_p2_score:
    df.loc[df["Hole"] == selected_hole, p1] = new_p1
    df.loc[df["Hole"] == selected_hole, p2] = new_p2
    st.session_state.score_data = df
    st.rerun()

st.divider()

# --- FULL SCORECARD SUMMARY TABLE ---
with st.expander("📋 View Full Scorecard Table", expanded=False):
    st.dataframe(df, hide_index=True, use_container_width=True)
