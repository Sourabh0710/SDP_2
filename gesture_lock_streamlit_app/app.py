import streamlit as st
from streamlit_drawable_canvas import st_canvas
from gesture_engine import GestureEngine
import time

st.set_page_config(page_title="Gesture Lock", layout="centered")

st.title("🔐 Gesture-Based Locking System")

# Initialize engine in session state
if 'engine' not in st.session_state:
    st.session_state.engine = GestureEngine()

if 'first_pattern' not in st.session_state:
    st.session_state.first_pattern = None
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

st.markdown("### Draw your pattern")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=4,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=300,
    width=300,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.json_data and canvas_result.json_data["objects"]:
    points = [(p["x"], p["y"]) for p in canvas_result.json_data["objects"] if "x" in p and "y" in p]
    
    if st.button("Submit Pattern"):
        if not st.session_state.first_pattern:
            st.session_state.first_pattern = points
            st.success("✅ First pattern captured. Please confirm by drawing it again.")
            time.sleep(1)
            st.rerun()
        else:
            if st.session_state.engine.is_match(st.session_state.first_pattern, points):
                st.session_state.engine.save_pattern(st.session_state.first_pattern)
                st.session_state.confirmed = True
                st.success("🎉 Pattern confirmed and saved securely!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Patterns do not match. Please start again.")
                st.session_state.first_pattern = None
                time.sleep(1)
                st.rerun()

if st.session_state.confirmed:
    st.markdown("---")
    st.markdown("### 📂 GitHub-style Project Files")
    st.code("""
📁 gesture_lock_streamlit_app/
├── app.py               # Streamlit UI
├── gesture_engine.py    # Pattern processing & encryption
├── key.key              # Fernet encryption key
├── patterns.dat         # Saved gesture pattern (encrypted)
├── unlock_attempts.log  # Log file for unlock attempts
├── requirements.txt     # For deployment
""")
