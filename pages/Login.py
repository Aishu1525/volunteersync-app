import streamlit as st

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    users = st.session_state.get("users", {})

    if username in users and users[username]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success("✅ Login successful! Go to Dashboard.")
    else:
        st.error("❌ Invalid credentials")