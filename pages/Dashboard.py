import streamlit as st
import pandas as pd
import random
from google import genai

# ---------------------------
# PAGE CONFIG (FIRST)
# ---------------------------
st.set_page_config(layout="wide")

# ---------------------------
# API SETUP
# ---------------------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found")
    st.stop()

client = genai.Client(api_key=api_key)
st.title("Gemini Test")

if st.button("Test Gemini"):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello"
    )
    st.write(response.text)
# ---------------------------
# VOLUNTEERS DATA
# ---------------------------
volunteers = [
    {"name": "Asha", "skills": "teaching, english", "location": "Guntur", "availability": "weekends"},
    {"name": "Rahul", "skills": "medical, first aid", "location": "Vijayawada", "availability": "full-time"},
    {"name": "Divya", "skills": "data entry, admin", "location": "Guntur", "availability": "weekdays"}
]

# ---------------------------
# AI MATCH FUNCTION (FIXED)
# ---------------------------
def smart_match(task, volunteers):
    if not task.strip():
        return "⚠️ Please enter a task"

    volunteers_text = "\n".join([
        f"{v['name']} | Skills: {v['skills']} | Location: {v['location']} | Availability: {v['availability']}"
        for v in volunteers
    ])

    prompt = f"""
You are an AI system that matches volunteers to tasks.

TASK:
{task}

VOLUNTEERS:
{volunteers_text}

Give:
- Top 3 best matches
- Reason for each
- Keep it short
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ---------------------------
# UI DESIGN
# ---------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2ff, #e0f7fa, #f5f3ff);
}

h1 {
    color: #4f46e5;
    text-align: center;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION INIT
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
# LOGIN CHECK
# ---------------------------
if not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.stop()

user = st.session_state.users.get(st.session_state.current_user)

if not user:
    st.error("User not found. Please login again.")
    st.stop()

# ---------------------------
# DASHBOARD HEADER
# ---------------------------
st.title("⚡ Volunteer Dashboard")
st.subheader(f"Welcome, {user['name']} 👋")

# ---------------------------
# SAMPLE TASKS
# ---------------------------
if len(st.session_state.tasks) == 0:
    st.session_state.tasks = [
        {"task": "Medical Camp Support", "location": "Guntur", "skill": "medical", "urgency": "High"},
        {"task": "Food Distribution Drive", "location": "Vijayawada", "skill": "food", "urgency": "Medium"},
        {"task": "Teaching Support", "location": "Guntur", "skill": "teaching", "urgency": "Low"}
    ]

tasks = st.session_state.tasks
df = pd.DataFrame(tasks)

# ---------------------------
# METRICS
# ---------------------------
col1, col2 = st.columns(2)
col1.metric("👥 Volunteers", len(st.session_state.users))
col2.metric("📌 Tasks", len(tasks))

# ---------------------------
# TASK INPUT FOR AI
# ---------------------------
st.markdown("## 🤖 Smart Matching")

task = st.text_area("Enter NGO Task Description")

if st.button("Find Best Volunteers"):
    if task:
        result = smart_match(task, volunteers)
        st.markdown("### ✅ AI Recommendations")
        st.write(result)
    else:
        st.warning("Please enter a task")

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
# RANDOM ALERT
# ---------------------------
if random.random() > 0.7:
    st.info("⚡ New urgent request just arrived!")
