import streamlit as st
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

