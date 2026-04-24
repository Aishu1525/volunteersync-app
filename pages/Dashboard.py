import streamlit as st
import random

st.set_page_config(layout="wide")

# Check login
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please login first!")
    st.stop()

user = st.session_state.users[st.session_state.current_user]

st.title("⚡ Volunteer Dashboard")
st.subheader(f"Welcome, {user['name']} 👋")

# Initialize tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ---------------------------
# CREATE TASK (LIVE DATA)
# ---------------------------
st.markdown("## 📌 Create New Task")

col1, col2 = st.columns(2)

with col1:
    task_name = st.text_input("Task Title")
    task_location = st.text_input("Task Location")

with col2:
    task_skill = st.selectbox("Required Skill", ["Medical", "Food Distribution", "Logistics", "Teaching"])
    task_urgency = st.selectbox("Urgency", ["High", "Medium", "Low"])

if st.button("➕ Add Task"):
    st.session_state.tasks.append({
        "task": task_name,
        "location": task_location,
        "skill": task_skill,
        "urgency": task_urgency
    })
    st.success("✅ Task Added Successfully!")

# ---------------------------
# AVAILABILITY
# ---------------------------
st.markdown("## ⏰ Availability")
availability = st.radio("Are you available?", ["Yes", "No"])

# ---------------------------
# MATCHING LOGIC
# ---------------------------
def calculate_score(user, task):
    score = 0

    if task["skill"] in user["skills"]:
        score += 50

    if task["location"].lower() == user["location"].lower():
        score += 30

    if task["urgency"] == "High":
        score += 30
    elif task["urgency"] == "Medium":
        score += 15

    return score

# ---------------------------
# ASSIGN TASK
# ---------------------------
if availability == "Yes":

    tasks = st.session_state.tasks

    if not tasks:
        st.warning("⚠️ No tasks available right now.")
    else:
        best_task = None
        best_score = -1

        for task in tasks:
            score = calculate_score(user, task)
            if score > best_score:
                best_score = score
                best_task = task

        st.success("✅ Task Assigned!")

        st.markdown(f"""
        ### 📌 Task: {best_task['task']}
        📍 Location: {best_task['location']}  
        ⚡ Urgency: {best_task['urgency']}  
        🧠 Required Skill: {best_task['skill']}
        """)

        st.markdown("""
        ### 🤖 Why you were selected:
        ✔ Skill match  
        ✔ Nearby location  
        ✔ Availability  
        ✔ Priority handling  
        """)

        if best_task["urgency"] == "High":
            st.error("🚨 HIGH PRIORITY TASK")

# ---------------------------
# LIVE DASHBOARD
# ---------------------------
st.markdown("## 📊 Live System Data")

st.write("👥 Total Volunteers:", len(st.session_state.users))
st.write("📌 Total Tasks:", len(st.session_state.tasks))

# ---------------------------
# INTERACTIVE FEATURE
# ---------------------------
if st.button("🎲 Get Motivation"):
    quotes = [
        "Your help can save lives ❤️",
        "Small actions create big impact 🌍",
        "Be the reason someone smiles today 😊"
    ]
    st.success(random.choice(quotes))

# ---------------------------
# RANDOM LIVE ALERT
# ---------------------------
if random.random() > 0.7:
    st.info("⚡ New urgent request just arrived!")