import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import os
from gesture_engine import GestureEngine

if 'engine' not in st.session_state:
    st.session_state.engine = GestureEngine()
    if st.session_state.engine.stage == "unlock":
        st.session_state.unlocked = False
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

st.set_page_config(page_title="Gesture Lock File Manager", layout="centered")
st.title("🔐 Gesture-Based Lock System")

canvas_result = st_canvas(
    fill_color="rgba(255,165,0,0.3)",
    stroke_width=5,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=300,
    width=300,
    drawing_mode="freedraw",
    key="canvas"
)

def extract_points(canvas_json):
    if not canvas_json or not canvas_json["objects"]:
        return []
    points = []
    for obj in canvas_json["objects"]:
        path = obj.get("path", [])
        for segment in path:
            if isinstance(segment, list) and len(segment) >= 3:
                x, y = segment[1], segment[2]
                points.append((x, y))
    return points

if st.button("Submit Pattern"):
    points = extract_points(canvas_result.json_data)
    if len(points) < 10:
        st.warning("Please draw a longer pattern.")
    else:
        message = st.session_state.engine.process_pattern(points)
        if message == "Unlocked!":
            st.session_state.unlocked = True
        st.success(message)

if st.session_state.unlocked:
    st.success("✅ Access Granted")
    st.subheader("📁 File Manager")

    current_dir = st.text_input("Enter directory", value=os.getcwd())
    try:
        files = os.listdir(current_dir)
        selected_file = st.selectbox("Select a file", files)
        file_path = os.path.join(current_dir, selected_file)

        if os.path.isfile(file_path):
            st.markdown(f"**File selected:** `{selected_file}`")
            if file_path.lower().endswith(('.txt', '.py', '.md')):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                st.text_area("📄 File content", content, height=300)
            else:
                st.write(f"Size: {os.path.getsize(file_path)} bytes")
        else:
            st.warning("Not a valid file.")
    except Exception as e:
        st.error(f"Error accessing directory: {e}")
