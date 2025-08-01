import streamlit as st
import json

# Set the page configuration
st.set_page_config(page_title="Register", page_icon="📝")

st.title("📝 Create a New Account")

# Helper function to load and save user data
def load_user_data():
    try:
        with open('data/user.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open('data/user.json', 'w') as f:
        json.dump(data, f, indent=2)

# --- Registration Form ---
with st.form("registration_form"):
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    # REMOVED: Email input and subscription checkboxes are gone.
    
    submitted = st.form_submit_button("Register")

    if submitted:
        users = load_user_data()
        
        # --- Form Validation ---
        # REMOVED: Email validation check is gone.
        if not all([new_username, new_password, confirm_password]):
            st.error("Please fill out all fields.")
        elif new_username in users:
            st.error("Username already exists. Please choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # --- Add new user ---
            # REMOVED: 'email' and 'subscriptions' keys are no longer added.
            users[new_username] = {
                "password": new_password,
                "role": "User",  # All new sign-ups are 'User' by default
            }
            save_user_data(users)
            st.success("Registration successful! You can now log in from the Home page.")
            st.balloons()