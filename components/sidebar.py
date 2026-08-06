import streamlit as st
from components.main_body import init_vars, reset_session
import uuid
import json



def render_sidebar():
    """
    Settings for sidebar
    """

    with st.sidebar:
        st.sidebar.title("Start New Session")
        st.sidebar.caption("Clears all current data and start new")
        if st.sidebar.button(label="New Session"):
            reset_session()
            st.sidebar.success("New Session Started!") 

        st.sidebar.title("Download Logs")
        st.sidebar.caption("Get current session history")
        
        st.download_button(label="Download logs",
                            data=json.dumps([{"session_history": st.session_state.messages[1:]}]),  # skip the system prompt
                            file_name=f"session_logs_{st.session_state.session_id}",
                            mime="application/json")

            
        