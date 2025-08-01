import streamlit as st
import json
import os

st.set_page_config(page_title="Admin Dashboard", page_icon="🔑")

# --- Admin Role Check ---
if st.session_state.get('role') != 'Admin':
    st.error("🚫 Access Denied. This page is for Admins only.")
    st.stop()

# --- Helper Functions ---
def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# --- Load Data for User Submissions ---
pending_stories = load_data('data/pending_stories.json')
approved_stories = load_data('data/approved_stories.json')

# --- UI for User Submission Review ---
st.title("🔑 Admin Dashboard")
st.write("Review and manage user submissions.")
st.header("Pending Submissions")

if not pending_stories:
    st.info("No pending submissions to review.")
else:
    # (The existing code for reviewing user stories remains here)
    for i, story in enumerate(pending_stories):
        with st.expander(f"Review: '{story['festival']}' story from {story['author']}"):
            st.subheader(f"Festival: {story['festival']}")
            st.write(f"**Region:** {story['region']}")
            st.write(f"**Author:** {story['author']}")
            st.write(f"**Story:**")
            st.info(story['story'])
            
            if os.path.exists(story['image_path']):
                st.image(story['image_path'], caption="Image submitted by user", width=300)
            else:
                st.warning("Image file not found.")

            col1, col2, col3 = st.columns([1, 1, 4])
            
            with col1:
                if st.button("Approve", key=f"approve_{story['id']}"):
                    story.pop('status', None)
                    approved_stories.append(story)
                    pending_stories.pop(i)
                    save_data('data/approved_stories.json', approved_stories)
                    save_data('data/pending_stories.json', pending_stories)
                    st.success("Story approved and published!")
                    st.rerun()

            with col2:
                if st.button("Reject", key=f"reject_{story['id']}"):
                    if os.path.exists(story['image_path']):
                        os.remove(story['image_path'])
                    pending_stories.pop(i)
                    save_data('data/pending_stories.json', pending_stories)
                    st.warning("Story rejected and image deleted.")
                    st.rerun()

st.divider()

# --- NEW SECTION: Add a Featured Festival Story ---
st.header("Add or Update a Featured Festival Story")
st.write("This story will appear on the 'Festival Highlights' page.")

featured_stories = load_data('data/featured_stories.json')

with st.form("featured_story_form", clear_on_submit=True):
    festival_name = st.text_input("Festival Name")
    main_story = st.text_area("Main Story (The primary description)")
    background_story = st.text_area("Background / History (Optional)")
    featured_image = st.file_uploader("Upload a feature image", type=['png', 'jpg', 'jpeg'])
    
    submitted = st.form_submit_button("Save Featured Story")

    if submitted:
        if not all([festival_name, main_story, featured_image]):
            st.error("Please provide a Festival Name, Main Story, and an Image.")
        else:
            # Save the uploaded image
            image_filename = f"featured_{festival_name.lower().replace(' ', '_')}.{featured_image.name.split('.')[-1]}"
            image_path = os.path.join("uploads", image_filename)
            with open(image_path, "wb") as f:
                f.write(featured_image.getbuffer())
            
            # Check if the festival story already exists to update it
            existing_story = next((s for s in featured_stories if s['festival_name'] == festival_name), None)
            
            if existing_story:
                # Update existing story
                existing_story['main_story'] = main_story
                existing_story['background_story'] = background_story
                existing_story['image_path'] = image_path
                st.success(f"Successfully updated the featured story for {festival_name}!")
            else:
                # Add new story
                new_featured_story = {
                    "festival_name": festival_name,
                    "main_story": main_story,
                    "background_story": background_story,
                    "image_path": image_path
                }
                featured_stories.append(new_featured_story)
                st.success(f"Successfully added {festival_name} as a new featured story!")
            
            save_data('data/featured_stories.json', featured_stories)