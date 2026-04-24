import streamlit as st

st.title("📝 Volunteer Registration")

if "users" not in st.session_state:
    st.session_state.users = {}

name = st.text_input("Full Name")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
location = st.text_input("Location")

skills = st.multiselect(
    "Select your skills",
    ["Medical", "Food Distribution", "Logistics", "Teaching"]
)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username in st.session_state.users:
        st.error("Username already exists!")
    else:
        st.session_state.users[username] = {
            "name": name,
            "gender": gender,
            "location": location,
            "skills": skills,
            "password": password
        }
        st.success("✅ Registered successfully! Go to Login page.")