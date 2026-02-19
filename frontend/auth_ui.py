import streamlit as st
from api import register, login, create_session

def auth_page():
    st.title("Text-to-SQL Analytics")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = login(email, password)
            if res.status_code == 200:
                token = res.json()["token"]

                session_res = create_session(token)
                session_id = session_res.json()["session_id"]

                st.session_state.token = token
                st.session_state.session_id = session_id
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email_r = st.text_input("Email ", key="reg_email")
        password_r = st.text_input("Password ", type="password", key="reg_pass")

        if st.button("Register"):
            res = register(email_r, password_r)
            if res.status_code == 200:
                st.success("Registered! Please login.")
            else:
                st.error("Registration failed")
