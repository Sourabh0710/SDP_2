import streamlit as st
from streamlit_drawable_canvas import st_canvas
from gesture_engine import GestureEngine
import time

st.set_page_config(page_title="Gesture Lock", layout="centered")
st.title("🔐 Gesture-Based Locking System")

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = GestureEngine()
if 'first_pattern' not in st.session_state:
    st.session_state.first_pattern = None
if 'awaiting_second' not in st.session_state:
    st.session_state.awaiting_second = False
if 'pattern_set' not in st.session_state:
    st.session_state.pattern_set = False
if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = "initial"

# Draw canvas
st.markdown("### Draw your pattern below:")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=4,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=300,
    width=300,
    drawing_mode="freedraw",
    key=st.session_state.canvas_key,
)

# Extract points from drawing
def extract_points(json_data):
    if json_data and "objects" in json_data:
        return [(obj["path"][0][1], obj["path"][0][2]) for obj in json_data["objects"] if obj["type"] == "path"]
    return []

# Handle submission
if st.button("Submit Pattern"):
    points = extract_points(canvas_result.json_data)

    if not points:
        st.warning("⚠️ Please draw a valid pattern before submitting.")
    elif not st.session_state.first_pattern:
        st.session_state.first_pattern = points
        st.session_state.awaiting_second = True
        st.session_state.canvas_key = str(time.time())  # Force canvas reset
        st.success("✅ Pattern recorded. Please confirm by drawing it again.")
        st.rerun()
    elif st.session_state.awaiting_second:
        if st.session_state.engine.is_match(st.session_state.first_pattern, points):
            st.session_state.engine.save_pattern(st.session_state.first_pattern)
            st.session_state.pattern_set = True
            st.session_state.awaiting_second = False
            st.success("🎉 Pattern confirmed and saved securely!")
        else:
            st.error("❌ Patterns do not match. Please start again.")
            st.session_state.first_pattern = None
            st.session_state.awaiting_second = False
        st.session_state.canvas_key = str(time.time())  # Reset canvas for next try
        st.rerun()

# Show GitHub-like file tree
if st.session_state.pattern_set:
    st.markdown("---")
    st.markdown("### 📂 Project Structure")
    st.code(
        """gesture_lock_streamlit_app/
├── app.py               # Streamlit frontend
├── gesture_engine.py    # Pattern processing & encryption
├── key.key              # Encryption key
├── patterns.dat         # Encrypted gesture pattern
├── unlock_attempts.log  # Log file for unlock attempts
├── requirements.txt     # Dependencies for Streamlit deployment"""
    )
