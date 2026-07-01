import streamlit as st
import os
import json

from auth import login, signup
from blockchain import Blockchain
from file_hash import hash_file
from logger import log_action

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Blockchain File Verifier",
    page_icon="🔐",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>

/* Sidebar */
[data-testid="stSidebar"]{
    background-color: #111827;
}

/* Selectbox container */
[data-baseweb="select"] {
    background-color: #1f2937 !important;
    border-radius: 8px;
}

/* Selected value */
[data-baseweb="select"] div {
    background-color: #1f2937 !important;
    color: white !important;
    font-weight: bold !important;
}

/* Dropdown menu */
ul {
    background-color: #1f2937 !important;
}

li {
    background-color: #1f2937 !important;
    color: white !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- LOGIN ----------
if not st.session_state.logged_in:

    st.title("🔐 Blockchain File Integrity Checker")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):

            if login(user, pwd):

                st.session_state.logged_in = True
                st.session_state.username = user

                st.session_state.blockchain = Blockchain(user)

                os.makedirs(
                    f"uploads/{user}",
                    exist_ok=True
                )

                log_action(user, "Login")

                st.rerun()

            else:
                st.error("Invalid Credentials")

    with tab2:

        user = st.text_input("New Username")
        pwd = st.text_input("New Password", type="password")

        if st.button("Signup"):

            if signup(user, pwd):
                st.success("Account Created")
            else:
                st.error("User Already Exists")

    st.stop()

# ---------- USER ----------
username = st.session_state.username
blockchain = st.session_state.blockchain
user_folder = f"uploads/{username}"

# ---------- SIDEBAR ----------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add File",
        "Verify File",
        "View Files",
        "View Blockchain",
        "Audit Logs",
        "Delete File",
        "Logout"
    ]
)

# ---------- DASHBOARD ----------
if menu == "Dashboard":

    files = os.listdir(user_folder)

    st.title("📊 Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Files", len(files))
    c2.metric("Blocks", len(blockchain.chain))
    c3.metric("User", username)

# ---------- ADD FILE ----------
elif menu == "Add File":

    file = st.file_uploader("Upload File")

    if file:

        path = os.path.join(
            user_folder,
            file.name
        )

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        h = hash_file(path)

        blockchain.add_block(
            file.name,
            h
        )

        log_action(
            username,
            f"Uploaded {file.name}"
        )

        st.success("File Added Successfully")

# ---------- VERIFY ----------
elif menu == "Verify File":

    files = os.listdir(user_folder)

    selected = st.selectbox(
        "Select File",
        files
    )

    if st.button("Verify"):

        path = os.path.join(
            user_folder,
            selected
        )

        current_hash = hash_file(path)

        stored_hash = None

        for block in blockchain.chain:
            if block.filename == selected:
                stored_hash = block.file_hash

        if current_hash == stored_hash:
            st.success("✅ File Integrity Verified")
        else:
            st.error("❌ File Tampered")

# ---------- VIEW FILES ----------
elif menu == "View Files":

    search = st.text_input(
        "Search File"
    )

    files = os.listdir(user_folder)

    for file in files:

        if search.lower() in file.lower():

            st.write("📄", file)

# ---------- BLOCKCHAIN ----------
elif menu == "View Blockchain":

    for block in blockchain.chain:
        st.json(block.to_dict())

# ---------- AUDIT LOGS ----------
elif menu == "Audit Logs":

    with open(
        "action_logs.json",
        "r"
    ) as f:

        logs = json.load(f)

    st.json(logs)

# ---------- DELETE ----------
elif menu == "Delete File":

    files = os.listdir(user_folder)

    selected = st.selectbox(
        "Select File",
        files
    )

    if st.button("Delete"):

        os.remove(
            os.path.join(
                user_folder,
                selected
            )
        )

        log_action(
            username,
            f"Deleted {selected}"
        )

        st.success(
            "File Deleted"
        )

# ---------- LOGOUT ----------
elif menu == "Logout":

    log_action(
        username,
        "Logout"
    )

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()