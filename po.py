import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pilgrim's Oak Round", layout="centered")

# Page Title
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

    # Determine hole point value & tie value
    if h_hcp <= 6:
        win_val, tie_val = 9, 3
    elif h_hcp <= 12:
        win_val, tie_val = 6, 2
    else:
        win_val, tie_val = 3, 1

    # Award points when both scores are entered
    if g1 > 0 and g2 > 0:
        if net1 < net2:
            p1_pts += win_val
        elif net2 < net1:
            p2_pts += win_val
        else:
            p1_pts += tie_val
            p2_pts += tie_val

# --- TRANSPARENT POINTS BOXES WITH WHITE BORDER & LARGER FONT ---
st.divider()
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

# Determine hole point value for header (Styled in Green)
if hole_hcp <= 6:
    hole_pts_str = "<span style='color: green; font-weight: bold;'>9 PTS</span>"
elif hole_hcp <= 12:
    hole_pts_str = "<span style='color: green; font-weight: bold;'>6 PTS</span>"
else:
    hole_pts_str = "<span style='color: green; font-weight: bold;'>3 PTS</span>"

# Red Stroke Alert for ATN
atn_gets_stroke = hole_hcp <= p2_hcp if p2 == "ATN" else (hole_hcp <= p1_hcp if p1 == "ATN" else False)
stroke_badge = "🔴 <span style='color: red; font-weight: bold;'>(ATN GETS A STROKE)</span>" if atn_gets_stroke else ""

# Hole Information Line
st.markdown(
    f"#### Hole {selected_hole} &nbsp;|&nbsp; {hole_yards} Yds &nbsp;|&nbsp; Par {hole_par} &nbsp;|&nbsp; Hcp {hole_hcp} &nbsp;|&nbsp; {hole_pts_str} {stroke_badge}",
    unsafe_allow_html=True
)

st.write("")

# Current Scores in State
curr_p1 = int(df.loc[df["Hole"] == selected_hole, p1].values[0])
curr_p2 = int(df.loc[df["Hole"] == selected_hole, p2].values[0])

# Score Selection Buttons (2 through 8)
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

# Save updates to session state
if new_p1 != curr_p1 or new_p2 != curr_p2:
    df.loc[df["Hole"] == selected_hole, p1] = new_p1
    df.loc[df["Hole"] == selected_hole, p2] = new_p2
    st.session_state.score_data = df
    st.rerun()

st.divider()

# --- STYLED SCORECARD TABLE ---
def style_scorecard(data_df):
    style_df = pd.DataFrame("", index=data_df.index, columns=data_df.columns)
    
    # Center all columns by default
    style_df.loc[:, :] = "text-align: center;"

    for idx, row in data_df.iterrows():
        h_hcp = int(row["Hcp"])
        g1 = int(row[p1])
        g2 = int(row[p2])

        # Bold player score cells regardless of status
        style_df.loc[idx, p1] = "text-align: center; font-weight: bold;"
        style_df.loc[idx, p2] = "text-align: center; font-weight: bold;"

        if g1 > 0 and g2 > 0:
            s1 = 1 if h_hcp <= p1_hcp else 0
            s2 = 1 if h_hcp <= p2_hcp else 0

            net1 = g1 - s1
            net2 = g2 - s2

            if net1 < net2:
                # P1 Wins Hole (Green Box)
                style_df.loc[idx, p1] = "text-align: center; background-color: #D4EDDA; color: #155724; font-weight: bold; border: 1px solid #C3E6CB;"
            elif net2 < net1:
                # P2 Wins Hole (Green Box)
                style_df.loc[idx, p2] = "text-align: center; background-color: #D4EDDA; color: #155724; font-weight: bold; border: 1px solid #C3E6CB;"
            else:
                # Tie (Yellow Box on both scores)
                style_df.loc[idx, p1] = "text-align: center; background-color: #FFF3CD; color: #856404; font-weight: bold; border: 1px solid #FFEEBA;"
                style_df.loc[idx, p2] = "text-align: center; background-color: #FFF3CD; color: #856404; font-weight: bold; border: 1px solid #FFEEBA;"

    return style_df

styled_df = df.style.apply(style_scorecard, axis=None).set_table_styles(
    [{"selector": "th", "props": [("text-align", "center")]}]
)

with st.expander("📋 View Full Scorecard Table", expanded=False):
    st.dataframe(styled_df, hide_index=True, use_container_width=True)

st.divider()

# --- PLAYER SETUP & HANDICAPS (MOVED TO BOTTOM) ---
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
