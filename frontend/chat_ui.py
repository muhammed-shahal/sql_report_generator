import streamlit as st
import pandas as pd
from api import ask_question, export_session

def chat_tab():
    st.header("Ask Questions")

    question = st.text_input("Ask your data")

    if st.button("Send"):
        with st.spinner("Generating SQL and fetching preview..."):
            res = ask_question(
                st.session_state.token,
                st.session_state.session_id,
                question
            )

        if res.status_code == 200:
            data = res.json()

            st.session_state.last_query_id = data["query_id"]
            st.session_state.last_sql = data["generated_sql"]
            st.session_state.last_preview = data["preview_rows"]

    if "last_sql" in st.session_state:
        st.subheader("Generated SQL")
        st.code(st.session_state.last_sql)

        st.subheader("Preview")
        df = pd.DataFrame(st.session_state.last_preview)
        st.dataframe(df)

        if st.button("Export"):
            res = export_session(
                st.session_state.token,
                st.session_state.session_id,
                st.session_state.last_query_id
            )

            if res.status_code == 200:
                data = res.json()
                msg = data.get("message", "Export started!")

                # If backend says it's not actually successful
                if "success" in msg.lower():
                    st.success(msg)
                else:
                    st.error(msg)

            else:
                st.error("Export failed")
