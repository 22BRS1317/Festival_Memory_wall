import streamlit as st
import json
import os

st.set_page_config(page_title="Festival Highlights", page_icon="🌟")

st.title("🌟 Festival Highlights")
st.write("Discover the main stories and history behind key festivals, curated by our admin.")

# Load the featured stories data
def load_featured_stories():
    try:
        with open('data/featured_stories.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

stories = load_featured_stories()

if not stories:
    st.info("No featured stories have been added yet.")
else:
    # Create a list of festival names for the selectbox
    festival_names = [story['festival_name'] for story in stories]
    
    selected_festival_name = st.selectbox("Select a festival to learn more:", festival_names)
    
    # Find the story data for the selected festival
    selected_story = next((s for s in stories if s['festival_name'] == selected_festival_name), None)

    if selected_story:
        st.divider()
        
        # Display the image
        if os.path.exists(selected_story['image_path']):
            st.image(selected_story['image_path'], caption=f"An image representing {selected_story['festival_name']}")
        
        # Display the stories
        st.header(f"The Story of {selected_story['festival_name']}")
        st.markdown(selected_story['main_story'])
        
        if selected_story.get('background_story'):
            st.subheader("Background & History")
            st.markdown(selected_story['background_story'])