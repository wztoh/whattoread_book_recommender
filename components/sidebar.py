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
            #TODO
            # create new session id
            # clears all database and chathistory
            reset_session()
            st.sidebar.write("New Session Started!") # temp

        st.sidebar.title("Download Logs")
        st.sidebar.caption("Get current session history")
        #TODO 
        st.download_button(label="Download logs",
                            data=json.dumps([{"session_id": st.session_state.session_id}]),  # #TODO edit this data type
                            file_name=f"session_logs_{st.session_state.session_id}",
                            mime="text.plain")

            
        