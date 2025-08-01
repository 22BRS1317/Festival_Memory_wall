import streamlit as st
import json
import os

st.set_page_config(page_title="Memory Wall", page_icon="🖼️")

# --- Authentication Check ---
if not st.session_state.get('authenticated', False):
    st.error("Please log in from the Home page to view the Memory Wall.")
    st.stop()

# Function to load approved stories
def load_approved_stories():
    try:
        with open('data/approved_stories.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- UI ---
st.title("🖼️ Festival Memory Wall")
st.write("A vibrant collection of festival memories from our community.")

stories = load_approved_stories()

if not stories:
    st.info("No stories have been shared yet. Be the first!")
else:
    # --- Filtering Options ---
    festivals = ["All"] + sorted(list(set(s['festival'] for s in stories)))
    regions = ["All"] + sorted(list(set(s['region'] for s in stories)))
    
    col1, col2 = st.columns(2)
    selected_festival = col1.selectbox("Filter by Festival", festivals)
    selected_region = col2.selectbox("Filter by Region", regions)
    
    # Filter stories
    filtered_stories = stories
    if selected_festival != "All":
        filtered_stories = [s for s in filtered_stories if s['festival'] == selected_festival]
    if selected_region != "All":
        filtered_stories = [s for s in filtered_stories if s['region'] == selected_region]

    # --- Display Stories ---
    if not filtered_stories:
        st.warning("No stories match your filter criteria.")
    else:
        for story in reversed(filtered_stories): # Show newest first
            with st.container(border=True):
                
                # CHANGED: Display the image from its local path
                image_path = story.get('image_path')
                if image_path and os.path.exists(image_path):
                    st.image(image_path, caption=f"A glimpse of {story['festival']}")
                
                st.subheader(f"{story['festival']} in {story['region']}")
                st.markdown(f"> {story['story']}")
                st.caption(f"Shared by: {story['author']}")