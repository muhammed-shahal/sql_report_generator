import streamlit as st
import pandas as pd
from api import get_history, preview_history, export_history

def history_tab():
    st.header("Saved Queries")

    res = get_history(st.session_state.token)

    if res.status_code != 200:
        st.error("Failed to load history")
        return

    queries = res.json()

    for q in queries:
        with st.expander(f"{q['question']} (ID: {q['id']})"):
            st.code(q["sql_query"])

            col1, col2 = st.columns(2)

            if col1.button(f"Run Preview {q['id']}"):
                preview = preview_history(st.session_state.token, q["id"]).json()
                df = pd.DataFrame(preview["preview_rows"])
                st.dataframe(df)

            if col2.button(f"Export {q['id']}"):
                res = export_history(st.session_state.token, q["id"])
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
