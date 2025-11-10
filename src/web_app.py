# src/web_app.py
import streamlit as st
from robot import Robot
import os


# Build absolute path to logo in ../assets/logo.png
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_PATH  = os.path.join(ASSETS_DIR, "logo.png")

# --- Page Config ---
st.set_page_config(
    page_title="",                    # ← removes title text
    page_icon=LOGO_PATH,              # ← shows logo in tab
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        max-width: 420px;
        margin: 25px auto;
        padding: 25px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .cell {
        width: 70px;
        height: 70px;
        background: linear-gradient(145deg, #1a2a3a, #2a3e52);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            inset 0 2px 6px rgba(0,0,0,0.3),
            0 4px 12px rgba(0,0,0,0.2);
        overflow: hidden;
    }
    .cell:hover {
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    .rover {
        width: 50px;
        height: 50px;
        animation: rover-bounce 1.8s infinite ease-in-out;
        filter: drop-shadow(0 0 8px #00ff88);
    }
    @keyframes rover-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    .title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00c9ff, #92fe9d, #ff7e5f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0 8px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #a0e7ff;
        font-size: 1.2rem;
        margin-bottom: 35px;
        font-weight: 500;
    }
    .control-panel {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 18px;
        backdrop-filter: blur(14px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.15);
    }
    .report {
        background: linear-gradient(45deg, #00c9ff, #92fe9d);
        color: #000;
        padding: 14px 24px;
        border-radius: 14px;
        font-weight: 800;
        text-align: center;
        font-size: 1.3rem;
        margin-top: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        letter-spacing: 1px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- SVG Rover (Base + Rotated Versions) ---
# Define the base rover once, hidden
st.markdown("""
<svg width="0" height="0">
  <defs>
    <g id="rover-base">
      <!-- Body -->
      <ellipse cx="50" cy="60" rx="36" ry="24" fill="url(#body)" stroke="#00cc66" stroke-width="3"/>
      <!-- Cabin -->
      <path d="M 35 45 Q 50 35, 65 45 L 65 55 Q 50 62, 35 55 Z" fill="url(#window)" stroke="#3399ff" stroke-width="2"/>
      <!-- Wheels -->
      <circle cx="28" cy="74" r="12" fill="#333" stroke="#111" stroke-width="3"/>
      <circle cx="72" cy="74" r="12" fill="#333" stroke="#111" stroke-width="3"/>
      <!-- Antenna -->
      <line x1="50" y1="35" x2="50" y2="20" stroke="#ffcc00" stroke-width="3" stroke-linecap="round"/>
      <circle cx="50" cy="16" r="5" fill="#ff6600"/>
    </g>
    <linearGradient id="body" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00ff88"/>
      <stop offset="100%" stop-color="#00cc66"/>
    </linearGradient>
    <linearGradient id="window" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#66ccff"/>
      <stop offset="100%" stop-color="#3399ff"/>
    </linearGradient>
  </defs>
</svg>
""", unsafe_allow_html=True)

# --- Rover SVGs by Direction (rotation via SVG transform) ---
rover_svg = {
    "NORTH": '''
    <svg class="rover" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g transform="rotate(0 50 50)">
        <use href="#rover-base"/>
      </g>
    </svg>
    ''',
    "EAST": '''
    <svg class="rover" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g transform="rotate(90 50 50)">
        <use href="#rover-base"/>
      </g>
    </svg>
    ''',
    "SOUTH": '''
    <svg class="rover" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g transform="rotate(180 50 50)">
        <use href="#rover-base"/>
      </g>
    </svg>
    ''',
    "WEST": '''
    <svg class="rover" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g transform="rotate(-90 50 50)">
        <use href="#rover-base"/>
      </g>
    </svg>
    '''
}

# --- Title ---
try:
    import base64
    with open(LOGO_PATH, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height:40px; display:block; margin:0 auto;">'
except:
    logo_html = "<p style='font-weight:900; color:white; text-align:center; margin:0;'>Mars Rover</p>"

st.markdown(f"""
<div style="
    background: skyblue;
    padding: 12px 20px;
    border-radius: 0 0 18px 18px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
">
    {logo_html}
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="subtitle">Command your rover on the Martian surface</p>', unsafe_allow_html=True)


# --- Session State ---
if "robot" not in st.session_state:
    st.session_state.robot = Robot()
    st.session_state.placed = False
    st.session_state.last_report = None

robot = st.session_state.robot

# --- Layout ---
col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("### Command Center")
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
        with st.form("place_form", clear_on_submit=False):
            st.markdown("**Place Rover**")
            x = st.number_input("X", min_value=0, max_value=4, value=0, step=1)
            y = st.number_input("Y", min_value=0, max_value=4, value=0, step=1)
            f = st.selectbox("Facing", ["NORTH", "EAST", "SOUTH", "WEST"])
            placed = st.form_submit_button("PLACE", use_container_width=True)
            
            if placed:
                if robot.place(x, y, f):
                    st.session_state.placed = True
                    st.success(f"Rover placed at **{x},{y},{f}**")
                    st.session_state.last_report = None
                else:
                    st.error("Invalid coordinates!")

        if st.session_state.placed:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("MOVE", use_container_width=True):
                    robot.move()
                    st.rerun()
            with col_b:
                if st.button("LEFT", use_container_width=True):
                    robot.left()
                    st.rerun()
                    
            col_c, col_d = st.columns(2)
            with col_c:
                if st.button("RIGHT", use_container_width=True):
                    robot.right()
                    st.rerun()
            with col_d:
                if st.button("REPORT", use_container_width=True):
                    report = robot.report()
                    st.session_state.last_report = report
                    st.success(f"**{report}**")
                    st.balloons()

        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### Martian Surface")
    
    grid = [[""] * 5 for _ in range(5)]
    if st.session_state.placed:
        grid[4 - robot.y][robot.x] = robot.f

    html = '<div class="grid-container">'
    for row in grid:
        for cell in row:
            if cell:
                html += f'<div class="cell">{rover_svg[cell]}</div>'
            else:
                html += '<div class="cell">·</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

    if st.session_state.last_report:
        st.markdown(f'<div class="report">TELEMETRY: {st.session_state.last_report}</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #88aabb; font-size: 0.95rem; margin-top: 20px;'>"
    "Mars Rover Control • Streamlit • Real-Time Graphics"
    "</p>",
    unsafe_allow_html=True
)