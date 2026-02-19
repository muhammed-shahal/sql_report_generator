import streamlit as st
from auth_ui import auth_page
from chat_ui import chat_tab
from history_ui import history_tab

st.set_page_config(page_title="Text2SQL", layout="wide")

if "token" not in st.session_state:
    auth_page()
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "History"])

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    if page == "Chat":
        chat_tab()
    else:
        history_tab()
