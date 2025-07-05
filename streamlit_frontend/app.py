import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import date
import plotly.express as px
from dateutil.parser import parse as parse_date
import time
task_id = st.query_params.get("task_id", [None])[0]

if task_id:
    st.success(f"Redirected to Task ID: {task_id}")


# Load API_URL from .env
load_dotenv()
API_URL = os.getenv("API_URL")

# ---------- SESSION STATE ----------
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False

# ---------- API FUNCTIONS ----------
def get_headers():
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}

def login(username, password):
    res = requests.post("http://127.0.0.1:8000/api/token/", data={"username": username, "password": password})
    if res.status_code == 200:
        st.session_state["access_token"] = res.json()["access"]
        return True
    return False

def register(username, password):
    res = requests.post("http://127.0.0.1:8000/api/register/", data={"username": username, "password": password})
    return res.status_code == 201

def get_tasks():
    res = requests.get(API_URL, headers=get_headers())
    return res.json() if res.status_code == 200 else []

def create_task(title, description, category, priority, due_date):
    payload = {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "due_date": due_date
    }
    res = requests.post(API_URL, headers=get_headers(), json=payload)
    return res.status_code == 201

def mark_completed(task_id):
    task_url = f"{API_URL}{task_id}/"
    res = requests.patch(task_url, headers=get_headers(), json={"completed": True})
    return res.status_code == 200

def delete_task(task_id):
    task_url = f"{API_URL}{task_id}/"
    res = requests.delete(task_url, headers=get_headers())
    return res.status_code == 204

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="To-Do App", layout="wide")
st.title("📝 Django To-Do App (Streamlit UI)")

# Show Register Button only if not logged in
if not st.session_state["access_token"]:
    with st.sidebar:
        if st.button("📝 Need an account? Register"):
            st.session_state["show_register"] = True

# ---------- REGISTER (Only if not logged in) ----------
if not st.session_state["access_token"] and st.session_state["show_register"]:
    with st.form("register_form"):
        st.subheader("🔐 Create New Account")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        reg_btn = st.form_submit_button("Register")

        if reg_btn:
            if new_pass != confirm_pass:
                st.error("Passwords do not match!")
            elif register(new_user, new_pass):
                st.success("Registered! Now login.")
                st.session_state["show_register"] = False
                st.rerun()
            else:
                st.error("Registration failed.")
    st.stop()

# ---------- LOGIN ----------
if not st.session_state["access_token"]:
    with st.form("login_form"):
        st.subheader("🔐 Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if login(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Login failed.")
    st.stop()

# ---------- AFTER LOGIN ----------
# Auto-refresh and search bar
refresh_interval = st.sidebar.slider("🔁 Auto-refresh (sec)", 0, 30, 0)
search_query = st.sidebar.text_input("🔍 Search by title")

if refresh_interval:
    time.sleep(refresh_interval)
    st.rerun()

# ➕ Add New Task
with st.expander("➕ Add New Task"):
    with st.form("create_task_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        category = st.selectbox("Category", ["Work", "Personal", "Study", "Others"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due_date = st.date_input("Due Date", min_value=date.today())
        submitted = st.form_submit_button("Create Task")

        if submitted:
            if create_task(title, description, category, priority, due_date.strftime("%Y-%m-%d")):
                st.success("Task created successfully!")
                st.rerun()
            else:
                st.error("Failed to create task.")

# 📊 Dashboard
st.subheader("📊 Task Overview")
tasks = get_tasks()

# Search filter
if search_query:
    tasks = [t for t in tasks if search_query.lower() in t["title"].lower()]

if tasks:
    completed = sum(t["completed"] for t in tasks)
    pending = len(tasks) - completed

    chart_data = {"Status": ["Completed", "Pending"], "Count": [completed, pending]}
    fig = px.pie(
        chart_data,
        names="Status",
        values="Count",
        title="Task Completion Status",
        color="Status",  # Map color based on label
        color_discrete_map={
            "Completed": "green",
            "Pending": "red"
        }
    )
    st.plotly_chart(fig, use_container_width=True)


    # Task filters
    show_today = st.checkbox("📅 Show Only Today’s Tasks")
    if show_today:
        today = date.today()
        tasks = [t for t in tasks if parse_date(t["due_date"]).date() == today]

    show_pending = st.checkbox("⏳ Show Only Pending Tasks")
    if show_pending:
        tasks = [t for t in tasks if not t["completed"]]

    # Task List
    st.subheader("📋 Task List")
    for task in tasks:
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.markdown(f"**{task['title']}** ({task['category']} / {task['priority']})")
            st.markdown(f"_Due: {task['due_date']}_ — {task['description']}")
        with col2:
            if not task["completed"]:
                if st.button("✅ Done", key=f"done-{task['id']}"):
                    mark_completed(task["id"])
                    st.rerun()
            else:
                st.write("✅")
        with col3:
            if st.button("🗑️", key=f"del-{task['id']}"):
                delete_task(task["id"])
                st.rerun()
else:
    st.info("No tasks found.")
