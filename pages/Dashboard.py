import streamlit as st
import pandas as pd

import random

# ---------------------------
# PAGE CONFIG (MUST BE FIRST)
# ---------------------------
st.set_page_config(layout="wide")

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2ff, #e0f7fa, #f5f3ff);
}

[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-right: 1px solid rgba(0,0,0,0.05);
}

[data-testid="stSidebar"] * {
    color: #334155;
}

h1 {
    color: #4f46e5;
    text-align: center;
    font-weight: 700;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    padding: 8px 16px;
}

.stButton > button:hover {
    transform: scale(1.05);
    opacity: 0.9;
}

input, textarea {
    border-radius: 10px !important;
    border: 1px solid #e5e7eb !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# SAFE SESSION INIT (IMPORTANT FIX)
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------------------
# CHECK LOGIN
# ---------------------------
if not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.stop()

user = st.session_state.users.get(st.session_state.current_user)

if not user:
    st.error("User not found. Please login again.")
    st.stop()

# ---------------------------
# TITLE
# ---------------------------
st.title("⚡ Volunteer Dashboard")
st.subheader(f"Welcome, {user['name']} 👋")

# ---------------------------
# SAFE TASKS
# ---------------------------
# ---------------------------
# SAFE TASKS + SAMPLE DATA
# ---------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 👉 Add demo tasks if empty (for dashboard testing)
if len(st.session_state.tasks) == 0:
    st.session_state.tasks = [
        {
            "task": "Medical Camp Support",
            "location": "Guntur",
            "skill": "Medical",
            "urgency": "High"
        },
        {
            "task": "Food Distribution Drive",
            "location": "Vijayawada",
            "skill": "Food Distribution",
            "urgency": "Medium"
        },
        {
            "task": "School Teaching Support",
            "location": "Guntur",
            "skill": "Teaching",
            "urgency": "Low"
        },
        {
            "task": "Logistics Coordination",
            "location": "Hyderabad",
            "skill": "Logistics",
            "urgency": "High"
        }
    ]
tasks = st.session_state.get("tasks", [])

df = pd.DataFrame(tasks) if tasks else pd.DataFrame(columns=["task", "location", "urgency", "skill"])

# ---------------------------
# AVAILABILITY
# ---------------------------
st.markdown("## ⏰ Availability")
availability = st.radio("Are you available?", ["Yes", "No"])

# ---------------------------
# METRICS (SAFE)
# ---------------------------
col1, col2 = st.columns(2)

col1.metric("👥 Volunteers", len(st.session_state.get("users", {})))
col2.metric("📌 Tasks", len(tasks))

# ---------------------------
# GRAPHS (SAFE CHECKS)
# ---------------------------
if not df.empty:

    st.markdown("## 🧠 Skill Demand")
    skill_counts = df["skill"].value_counts()


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
# TASK ASSIGNMENT
# ---------------------------
if availability == "Yes":

    if not tasks:
        st.warning("⚠️ No tasks available right now.")
    else:

        best_task = max(tasks, key=lambda t: calculate_score(user, t))

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
# LIVE DATA
# ---------------------------
st.markdown("## 📊 Live System Data")

st.write("👥 Total Volunteers:", len(st.session_state.get("users", {})))
st.write("📌 Total Tasks:", len(tasks))

# ---------------------------
# MOTIVATION
# ---------------------------
if st.button("🎲 Get Motivation"):
    quotes = [
        "Your help can save lives ❤️",
        "Small actions create big impact 🌍",
        "Be the reason someone smiles today 😊"
    ]
    st.success(random.choice(quotes))

# ---------------------------
# ALERT
# ---------------------------
if random.random() > 0.7:
    st.info("⚡ New urgent request just arrived!")  