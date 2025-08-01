import streamlit as st
import json
from streamlit_calendar import calendar
from datetime import datetime

st.set_page_config(page_title="Festival Calendar", page_icon="🗓️", layout="wide")

# --- Authentication Check ---
if not st.session_state.get('authenticated', False):
    st.error("Please log in to view the calendar.")
    st.stop()

# Load festival dates from JSON
def load_festival_events():
    try:
        with open('data/festival_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- UI ---
st.title("🗓️ Festival Calendar 2025")
st.write("Here are the major festival dates for the upcoming year.")

all_events = load_festival_events()

calendar_options = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,dayGridWeek,timeGridDay",
    },
    "initialView": "dayGridMonth",
    "initialDate": "2025-08-01", # Set the initial calendar view to the current date
}

# The calendar component
calendar(events=all_events, options=calendar_options, key="festival_calendar")

st.divider()

# --- NEW: Display Festivals for the Current Month in a Styled Format ---
st.header("Festivals This Month")

# Get today's date to determine the current month
today = datetime.now()
current_month = today.month
current_year = today.year

# Filter events for the current month
monthly_events = [
    event for event in all_events
    if datetime.strptime(event['start'], '%Y-%m-%d').month == current_month and
       datetime.strptime(event['start'], '%Y-%m-%d').year == current_year
]

if not monthly_events:
    st.info(f"No major festivals are scheduled for {today.strftime('%B %Y')}.")
else:
    for event in monthly_events:
        # Format the date for display
        start_date = datetime.strptime(event['start'], '%Y-%m-%d')
        date_str = start_date.strftime('%B %d, %Y')
        
        # Display each festival in a styled container
        with st.container(border=True):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"<h3 style='text-align: center; color: {event.get('color', '#FFFFFF')};'>{start_date.strftime('%d')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{start_date.strftime('%b')}</p>", unsafe_allow_html=True)
            with col2:
                st.subheader(event['title'])
                st.write(event.get('description', 'No description available.'))