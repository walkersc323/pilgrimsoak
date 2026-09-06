import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pilgrim's Oak Round", layout="centered")

# Page Title & Subtitle
st.markdown("### ⛳ Pilgrim's Oak Round")
st.caption("White / Gold Tees • Par 72 • 5,828 Yards")

# --- INITIALIZE PLAYERS & HANDICAPS IN SESSION STATE ---
if "p1_name" not in st.session_state:
    st.session_state.p1_name = "SCW"
if "p1_hcp" not in st.session_state:
    st.session_state.p1_hcp = 0
if "p2_name" not in st.session_state:
    st.session_state.p2_name = "ATN"
if "p2_hcp" not in st.session_state:
    st.session_state.p2_hcp = 12

p1 = st.session_state.p1_name
p1_hcp = st.session_state.p1_hcp
p2 = st.session_state.p2_name
p2_hcp = st.session_state.p2_hcp

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

# --- CALCULATE WALKER CUP POINTS ---
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
        win_val, tie_val = 9, 3
    elif h_hcp <= 12:
        win_val, tie_val = 6, 2
    else:
        win_val, tie_val = 3, 1

    if g1 > 0 and g2 > 0:
        if net1 < net2:
            p1_pts += win_val
        elif net2 < net1:
            p2_pts += win_val
        else:
            p1_pts += tie_val
            p2_pts += tie_val

# --- TRANSPARENT POINTS BOXES DIRECTLY BELOW SUBTITLE ---
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f"""
        <div style="border: 2px solid #FFFFFF; border-radius: 8px; padding: 12px; text-align: center; background-color: transparent;">
            <span style="font-size: 16px; font-weight: bold;">{p1}</span><br>
            <span style="font-size: 40px; font-weight: 900;">{int(p1_pts)} PTS</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"""
        <div style="border: 2px solid #FFFFFF; border-radius: 8px; padding: 12px; text-align: center; background-color: transparent;">
            <span style="font-size: 16px; font-weight: bold;">{p2}</span><br>
            <span style="font-size: 40px; font-weight: 900;">{int(p2_pts)} PTS</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# --- HOLE SELECTOR ---
selected_hole = st.number_input("Select Hole Being Played", min_value=1, max_value=18, step=1, value=1)
hole_info = df[df["Hole"] == selected_hole].iloc[0]

hole_hcp = int(hole_info["Hcp"])
hole_par = int(hole_info["Par"])
hole_yards = int(hole_info["Yards"])

if hole_hcp <= 6:
    hole_pts_str = "<span style='color: green; font-weight: bold;'>9 PTS</span>"
elif hole_hcp <= 12:
    hole_pts_str = "<span style='color: green; font-weight: bold;'>6 PTS</span>"
else:
    hole_pts_str = "<span style='color: green; font-weight: bold;'>3 PTS</span>"

atn_gets_stroke = hole_hcp <= p2_hcp if p2 == "ATN" else (hole_hcp <= p1_hcp if p1 == "ATN" else False)
stroke_badge = "🔴 <span style='color: red; font-weight: bold;'>(ATN GETS A STROKE)</span>" if atn_gets_stroke else ""

st.markdown(
    f"#### Hole {selected_hole} &nbsp;|&nbsp; {hole_yards} Yds &nbsp;|&nbsp; Par {hole_par} &nbsp;|&nbsp; Hcp {hole_hcp} &nbsp;|&nbsp; {hole_pts_str} {stroke_badge}",
    unsafe_allow_html=True
)

st.write("")

curr_p1 = int(df.loc[df["Hole"] == selected_hole, p1].values[0])
curr_p2 = int(df.loc[df["Hole"] == selected_hole, p2].values[0])

score_options = [2, 3, 4, 5, 6, 7, 8]

st.markdown(f"**{p1}'s Gross Score:**")
p1_cols = st.columns(7)
new_p1 = curr_p1

for idx, val in enumerate(score_options):
    button_type = "primary" if curr_p1 == val else "secondary"
    if p1_cols[idx].button(str(val), key=f"p1_btn_{selected_hole}_{val}", type=button_type):
        new_p1 = val

st.markdown(f"**{p2}'s Gross Score:**")
p2_cols = st.columns(7)
new_p2 = curr_p2

for idx, val in enumerate(score_options):
    button_type = "primary" if curr_p2 == val else "secondary"
    if p2_cols[idx].button(str(val), key=f"p2_btn_{selected_hole}_{val}", type=button_type):
        new_p2 = val

if new_p1 != curr_p1 or new_p2 != curr_p2:
    df.loc[df["Hole"] == selected_hole, p1] = new_p1
    df.loc[df["Hole"] == selected_hole, p2] = new_p2
    st.session_state.score_data = df
    st.rerun()

st.divider()

# --- SCORECARD TABLE (HIGH CONTRAST GREEN/YELLOW BOLD SCORES + STROKE ASTERISK) ---
rows_html = ""
for _, row in df.iterrows():
    h = int(row["Hole"])
    y = int(row["Yards"])
    par = int(row["Par"])
    hcp = int(row["Hcp"])
    g1 = int(row[p1])
    g2 = int(row[p2])

    # Check strokes per hole
    s1 = 1 if hcp <= p1_hcp else 0
    s2 = 1 if hcp <= p2_hcp else 0

    # Red asterisk indicator for player stroke holes
    p1_ast = "<span style='color:#FF4B4B; font-weight:bold;'>*</span>" if s1 > 0 else ""
    p2_ast = "<span style='color:#FF4B4B; font-weight:bold;'>*</span>" if s2 > 0 else ""

    p1_val_str = f"{g1}{p1_ast}" if g1 > 0 else "-"
    p2_val_str = f"{g2}{p2_ast}" if g2 > 0 else "-"

    p1_cell = f"<span style='font-size:17px; font-weight:bold;'>{p1_val_str}</span>"
    p2_cell = f"<span style='font-size:17px; font-weight:bold;'>{p2_val_str}</span>"

    if g1 > 0 and g2 > 0:
        net1 = g1 - s1
        net2 = g2 - s2

        green_style = "background-color: #28A745; color: #000000; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 18px;"
        yellow_style = "background-color: #FFC107; color: #000000; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 18px;"

        if net1 < net2:
            p1_cell = f"<span style='{green_style}'>{p1_val_str}</span>"
        elif net2 < net1:
            p2_cell = f"<span style='{green_style}'>{p2_val_str}</span>"
        else:
            p1_cell = f"<span style='{yellow_style}'>{p1_val_str}</span>"
            p2_cell = f"<span style='{yellow_style}'>{p2_val_str}</span>"

    rows_html += f"<tr><td>{h}</td><td>{y}</td><td>{par}</td><td>{hcp}</td><td>{p1_cell}</td><td>{p2_cell}</td></tr>"

table_code = f"""
<style>
    .scorecard-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        margin-top: 10px;
    }}
    .scorecard-table th {{
        text-align: center !important;
        padding: 8px;
        border-bottom: 2px solid #666;
        font-size: 15px;
    }}
    .scorecard-table td {{
        text-align: center !important;
        padding: 8px;
        border-bottom: 1px solid #444;
        font-size: 15px;
    }}
</style>
<table class="scorecard-table">
    <thead>
        <tr>
            <th>Hole</th>
            <th>Yards</th>
            <th>Par</th>
            <th>Hcp</th>
            <th>{p1}</th>
            <th>{p2}</th>
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>
"""

with st.expander("📋 View Full Scorecard Table", expanded=False):
    st.html(table_code)

st.divider()

# --- PLAYER SETUP & HANDICAPS (AT BOTTOM) ---
with st.expander("⚙️ Player Setup & Handicaps", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        new_p1_name = st.text_input("Player 1 Name", value=p1)
        new_p1_hcp = st.number_input(f"{new_p1_name} Handicap", value=p1_hcp, min_value=0, max_value=36, step=1)
    with col2:
        new_p2_name = st.text_input("Player 2 Name", value=p2)
        new_p2_hcp = st.number_input(f"{new_p2_name} Handicap", value=p2_hcp, min_value=0, max_value=36, step=1)

    if new_p1_name != p1 or new_p2_name != p2 or new_p1_hcp != p1_hcp or new_p2_hcp != p2_hcp:
        st.session_state.p1_name = new_p1_name
        st.session_state.p1_hcp = new_p1_hcp
        st.session_state.p2_name = new_p2_name
        st.session_state.p2_hcp = new_p2_hcp
        st.rerun()
