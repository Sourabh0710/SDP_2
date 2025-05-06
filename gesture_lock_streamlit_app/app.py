import streamlit as st
from streamlit_drawable_canvas import st_canvas
from gesture_engine import GestureEngine

st.set_page_config(page_title="Gesture Lock", layout="centered")

# Initialize session state
if "engine" not in st.session_state:
    st.session_state.engine = GestureEngine()
if "first_pattern" not in st.session_state:
    st.session_state.first_pattern = None
if "pattern_verified" not in st.session_state:
    st.session_state.pattern_verified = False

st.title("🔒 Gesture Lock System")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#ffffff",
    update_streamlit=True,
    height=300,
    width=300,
    drawing_mode="freedraw",
    key="canvas_draw",
    disabled=st.session_state.pattern_verified
)

if canvas_result.json_data and canvas_result.json_data["objects"]:
    pattern_points = [
        (obj["left"], obj["top"])
        for obj in canvas_result.json_data["objects"]
        if obj["type"] == "path"
    ]
    if st.button("Submit Pattern"):
        if not st.session_state.first_pattern:
            st.session_state.first_pattern = pattern_points
            st.success("Pattern saved! Please re-draw to confirm.")
            st.experimental_rerun()
        else:
            if st.session_state.engine.compare_patterns(
                st.session_state.first_pattern, pattern_points
            ):
                st.success("Pattern confirmed and saved!")
                st.session_state.engine.save_pattern(pattern_points)
                st.session_state.pattern_verified = True
            else:
                st.error("Patterns do not match. Try again.")
                st.session_state.first_pattern = None
                st.experimental_rerun()

if st.session_state.pattern_verified:
    st.subheader("✅ Your pattern has been set successfully!")
    st.markdown("View the generated files:")
    st.code("📁 patterns.dat
🔑 key.key
📄 unlock_attempts.log", language="bash")