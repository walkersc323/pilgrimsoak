import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pilgrim's Oak Match", layout="centered")

st.title("⛳ Pilgrim's Oak Match")
st.caption("White / Gold Tees • Par 72 • 5,828 Yards")

# --- MATCH SETUP ---
col1, col2 = st.columns(2)
with col1:
    p1 = st.text_input("Player 1 Name", value="Player 1")
with col2:
    p2 = st.text_input("Player 2 Name", value="Player 2")

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

# Handle dynamic player name updates in table headers
df = st.session_state.score_data
if p1 not in df.columns:
    df.columns = ["Hole", "Yards", "Par", "Hcp", p1, df.columns[5]]
if p2 not in df.columns:
    df.columns = ["Hole", "Yards", "Par", "Hcp", df.columns[4], p2]

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

# --- CALCULATIONS & LEADERBOARD ---
p1_played = edited_df[edited_df[p1] > 0]
p2_played = edited_df[edited_df[p2] > 0]

p1_total = p1_played[p1].sum()
p2_total = p2_played[p2].sum()

p1_par = p1_played["Par"].sum()
p2_par = p2_played["Par"].sum()

p1_to_par = p1_total - p1_par
p2_to_par = p2_total - p2_par

st.divider()
st.subheader("Leaderboard")

m1, m2 = st.columns(2)

def format_score(to_par, total):
    if total == 0:
        return "E", "0 strokes"
    sign = "+" if to_par > 0 else ""
    str_to_par = "E" if to_par == 0 else f"{sign}{int(to_par)}"
    return str_to_par, f"{int(total)} strokes"

p1_str, p1_sub = format_score(p1_to_par, p1_total)
p2_str, p2_sub = format_score(p2_to_par, p2_total)

m1.metric(label=p1, value=p1_str, delta=p1_sub, delta_color="off")
m2.metric(label=p2, value=p2_str, delta=p2_sub, delta_color="off")

# Match Leaderboard Summary
if len(p1_played) > 0 and len(p2_played) > 0:
    diff = int(p1_total - p2_total)
    if diff < 0:
        st.info(f"🏆 **{p1}** leads by **{abs(diff)}** stroke{'s' if abs(diff) > 1 else ''}.")
    elif diff > 0:
        st.info(f"🏆 **{p2}** leads by **{diff}** stroke{'s' if diff > 1 else ''}.")
    else:
        st.info("🤝 The match is currently **Tied**.")
