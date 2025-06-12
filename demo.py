import streamlit as st
import requests

# ✅ Your n8n webhook URL
N8N_WEBHOOK_URL = "https://dhina04.app.n8n.cloud/webhook-test/4e2f2db0-17d2-4b94-a22a-6938f42a3dd7"

# ✅ Dummy login credentials (customize as needed)
VALID_USERS = {
    "admin": "password123",
    "john": "doe2024"
}

# --- Initialize session state ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Login function ---
def login():
    st.title("🔐 Employee Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password.")

# --- Logout function ---
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""

# --- Action Item Form ---
def action_form():
    st.title("📝 Submit Meeting Action Items")
    st.success(f"Welcome, **{st.session_state.username}**!")

    with st.form("action_form"):
        meeting_date = st.date_input("Meeting Date")
        action_item = st.text_area("Action Item")
        assigned_to = st.text_input("Assigned To")
        due_date = st.date_input("Due Date")
        email_id = st.text_input("Email ID")  # New Field
        submitted = st.form_submit_button("Submit")

        if submitted:
            payload = {
                "username": st.session_state.username,
                "meeting_date": str(meeting_date),
                "action_item": action_item,
                "assigned_to": assigned_to,
                "due_date": str(due_date),
                "email_id": email_id
            }

            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("✅ Action item submitted successfully!")
                else:
                    st.error(f"❌ Submission failed with status code {response.status_code}")
                    st.code(response.text)
            except Exception as e:
                st.error(f"❌ Error sending data: {e}")

    if st.button("Logout"):
        logout()
        st.experimental_rerun()

# --- Main App Logic ---
def main():
    if st.session_state.authenticated:
        action_form()
    else:
        login()

if __name__ == "__main__":
    main()
