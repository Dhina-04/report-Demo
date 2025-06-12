import streamlit as st
import requests

# Replace with your actual webhook URL
N8N_WEBHOOK_URL = "https://dhina04.app.n8n.cloud/webhook-test/4e2f2db0-17d2-4b94-a22a-6938f42a3dd7"

# Dummy user credentials
VALID_USERS = {
    "admin": "password123",
    "D": "1243"
}

# --- Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Login Function ---
def login():
    st.title("🔐 Employee Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# --- Logout Function ---
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.experimental_rerun()

# --- Action Item Form ---
def action_form():
    st.title("📝 Submit Meeting Action Items")
    st.write(f"Welcome, **{st.session_state.username}**!")

    with st.form("action_form"):
        meeting_date = st.date_input("Meeting Date")
        action_item = st.text_area("Action Item")
        assigned_to = st.text_input("Assigned To")
        due_date = st.date_input("Due Date")
        submit = st.form_submit_button("Submit")

        if submit:
            payload = {
                "username": st.session_state.username,
                "meeting_date": str(meeting_date),
                "action_item": action_item,
                "assigned_to": assigned_to,
                "due_date": str(due_date)
            }

            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("Action item submitted successfully!")
                else:
                    st.error(f"Failed to submit. Status: {response.status_code}")
            except Exception as e:
                st.error(f"Error sending data: {e}")

    st.button("Logout", on_click=logout)

# --- Main App Logic ---
def main():
    if not st.session_state.authenticated:
        login()
    else:
        action_form()

if __name__ == "__main__":
    main()
