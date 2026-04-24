import streamlit as st
import random
st.markdown("""
<style>

/* 🌈 Main Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2ff, #e0f7fa, #f5f3ff);
}

/* 🧊 MODERN SIDEBAR (Glass Effect) */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-right: 1px solid rgba(0,0,0,0.05);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #334155;
}

/* 🟣 Title */
h1 {
    color: #4f46e5;
    text-align: center;
    font-weight: 700;
}

/* 🔹 Subheading */
h3 {
    color: #475569;
}

/* 🧊 Cards */
.card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* 🔘 Buttons (Main area) */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    padding: 8px 16px;
    transition: 0.3s;
}

/* ✨ Hover */
.stButton > button:hover {
    transform: scale(1.05);
    opacity: 0.9;
}

/* 🧭 SIDEBAR BUTTONS (make them look like nav items) */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent;
    color: #334155;
    text-align: left;
    border-radius: 10px;
    padding: 10px;
    font-weight: 500;
}

/* Sidebar button hover */
[data-testid="stSidebar"] .stButton > button:hover {
    background: #e0f2fe;
    transform: none;
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #e5e7eb !important;
}

/* Alerts */
.stSuccess { background-color: #dcfce7 !important; }
.stInfo { background-color: #e0f2fe !important; }
.stWarning { background-color: #fef9c3 !important; }
.stError { background-color: #fee2e2 !important; }

</style>
""", unsafe_allow_html=True)
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

