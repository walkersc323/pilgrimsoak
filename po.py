import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pilgrim's Oak - Walker Cup Match", layout="centered")

st.title("⛳ Pilgrim's Oak - Walker Cup Match")
st.caption("White / Gold Tees • Par 72 • 5,828 Yards")

# --- MATCH SETUP ---
col1, col2 = st.columns(2)
with col1:
    p1 = st.text_input("Player 1 Name", value="ATN")
    p1_hcp = st.number_input(f"{p1} Handicap Strokes", value=12, min_value=0, max_value=36, step=1)
with col2:
    p2 = st.text_input("Player 2 Name", value="Player 2")
    p2_hcp = st.number_input(f"{p2} Handicap Strokes", value=0, min_value=0, max_value=36, step=1)

st.divider()

# --- PILGRIM'S OAK WHITE/GOLD SCORECARD ---
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

# Ensure dynamic column header sync
if p1 not in df.columns or p2 not in df.columns:
    df.columns = ["Hole", "Yards", "Par", "Hcp", p1, p2]

st.subheader("Scorecard")

edited_df = st.data_editor(
    df,
    column_config={
        "Hole": st.column_config.NumberColumn("Hole", disabled=True),
        "Yards": st.column_config.NumberColumn("Yards", disabled=True),
        "Par": st.column_config.NumberColumn("Par", disabled=True),
        "Hcp": st.column_config.NumberColumn("Hcp", disabled=True),
        p1: st.column_config.NumberColumn(p1, min_value=0, max_value=15, step=1),
        p2: st.column_config.NumberColumn(p2, min_value=0, max_value=15, step=1),
    },
    hide_index=True,
    use_container_width=True
)

st.session_state.score_data = edited_df

# --- CALCULATIONS ---
p1_pts = 0
p2_pts = 0
p1_gross_tot = 0
p2_gross_tot = 0

for _, row in edited_df.iterrows():
    h_hcp = row["Hcp"]
    g1 = row[p1]
    g2 = row[p2]

    # Calculate stroke handicaps per hole
    p1_strokes = 1 if h_hcp <= p1_hcp else 0
    p2_strokes = 1 if h_hcp <= p2_hcp else 0

    net1 = g1 - p1_strokes if g1 > 0 else 0
    net2 = g2 - p2_strokes if g2 > 0 else 0

    # Determine hole point value
    if h_hcp <= 6:
        hole_val = 9
    elif h_hcp <= 12:
        hole_val = 6
    else:
        hole_val = 3

    # Award points if both players entered gross scores
    if g1 > 0 and g2 > 0:
        p1_gross_tot += g1
        p2_gross_tot += g2

        if net1 < net2:
            p1_pts += hole_val
        elif net2 < net1:
            p2_pts += hole_val
        else:
            p1_pts += hole_val // 2
            p2_pts += hole_val // 2

st.divider()

# --- WALKER CUP POINTS LEADERBOARD ---
st.subheader("🏆 Walker Cup Points Leaderboard")

c1, c2 = st.columns(2)
c1.metric(label=f"{p1} Points", value=f"{int(p1_pts)} pts", delta=f"{int(p1_gross_tot)} Gross Strokes", delta_color="off")
c2.metric(label=f"{p2} Points", value=f"{int(p2_pts)} pts", delta=f"{int(p2_gross_tot)} Gross Strokes", delta_color="off")

# Status Banner
diff = int(p1_pts - p2_pts)
if p1_gross_tot > 0 and p2_gross_tot > 0:
    if diff > 0:
        st.info(f"🚩 **{p1}** leads by **{diff}** point{'s' if diff > 1 else ''}.")
    elif diff < 0:
        st.info(f"🚩 **{p2}** leads by **{abs(diff)}** point{'s' if abs(diff) > 1 else ''}.")
    else:
        st.info("🤝 The match is currently **Tied**.")
