import streamlit as st
import json
import time
import os
from datetime import datetime

st.set_page_config(page_title="Share Your Story", page_icon="✍️")

# --- Authentication Check ---
if not st.session_state.get('authenticated', False):
    st.error("Please log in to share your story.")
    st.stop()

# Function to save a pending story
def save_pending_story(story_data):
    try:
        with open('data/pending_stories.json', 'r+', encoding='utf-8') as f:
            stories = json.load(f)
            stories.append(story_data)
            f.seek(0)
            json.dump(stories, f, indent=2)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('data/pending_stories.json', 'w', encoding='utf-8') as f:
            json.dump([story_data], f, indent=2)

# --- UI ---
st.title("✍️ Share Your Festival Memory")
st.write("We'd love to hear how you celebrate! Your story will be reviewed by an admin before being published.")

with st.form("story_form", clear_on_submit=True):
    author = st.text_input("Your Name / Alias", value=st.session_state.get('username', ''))

    # Users can now type any festival name
    festival = st.text_input("Festival Name (e.g., Diwali, Eid, Onam)")
    
    # ADDED: Users can now add the date of their story
    story_date = st.date_input("Date of the memory", value="today")

    region = st.text_input("Your Region (e.g., Chennai, Tamil Nadu)")
    story = st.text_area("Your Story", height=200, placeholder="Describe the rituals, emotions, and unique traditions...")
    
    # Users can now upload their own image
    uploaded_image = st.file_uploader("Upload an image for your story", type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button("Submit for Review")

    if submitted:
        if not all([author, festival, region, story, uploaded_image, story_date]):
            st.error("Please fill out all the fields and upload an image.")
        else:
            # Create a unique ID for the story
            story_id = str(int(time.time()))
            
            # Save the uploaded image to the 'uploads' folder
            image_path = os.path.join("uploads", f"{story_id}.{uploaded_image.name.split('.')[-1]}")
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            story_data = {
                "id": story_id,
                "author": author,
                "festival": festival,
                "region": region,
                "story": story,
                "image_path": image_path,
                "story_date": story_date.strftime("%Y-%m-%d"), # Store the date as a string
                "status": "pending"
            }
            save_pending_story(story_data)
            st.success("Thank you! Your story has been submitted for review.")