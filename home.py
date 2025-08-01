import streamlit as st
import json
import time

# Set page configuration
st.set_page_config(
    page_title="Festival Memory Wall",
    page_icon="🎉",
    layout="centered"
)

# Function to load user data
def load_users():
    # This line is already changed to match your filename 'user.json'
    with open('data/user.json', 'r') as f:
        return json.load(f)

# --- UI ---
st.title("🎉 Welcome to the Festival Memory Wall!")
st.write("""
    Share your unique festival traditions and discover how others celebrate across the world.
    Please log in to continue.
""")

# Initialize session state for login
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['username'] = ""
    st.session_state['role'] = ""

# --- Login Logic ---
if not st.session_state['authenticated']:
    users_db = load_users()
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in users_db and users_db[username]['password'] == password:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['role'] = users_db[username]['role']
                st.rerun() # Rerun the script to reflect the new state
            else:
                st.error("Incorrect username or password")
    
    # --- ADDED THIS LINE ---
    st.info("New user? Select 'register' from the sidebar to create an account.")


# --- Post-Login UI ---
if st.session_state['authenticated']:
    st.success(f"Logged in as **{st.session_state['username']}** (`{st.session_state['role']}`)")
    st.write("Select a page from the sidebar to get started.")

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = ""
        st.session_state['role'] = ""
        st.rerun()