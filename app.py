import streamlit as st
import config
import uuid

from components.header import render_header
from components.sidebar import render_sidebar
import components.main_body as components_body



# init vars
components_body.init_vars()


# setting up default web UI
st.set_page_config(page_title="WhatToRead")
render_header()
render_sidebar()

selected_title = components_body.title_input()
selected_author = components_body.author_input()
components_body.genre_selection()
components_body.clear_genre_selection_button()

# main body code
# testing code (to remove)
#TODO remove testing code
# st.write(st.session_state.session_id)
# if input := st.text_input("Write here"):
#     st.write(input)
# st.write("session genre_pills: ",st.session_state.genre_pills)

# st.write(f"title:{a}, author:{b}")

