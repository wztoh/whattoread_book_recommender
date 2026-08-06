import streamlit as st
import config
import uuid

from components.header import render_header
from components.sidebar import render_sidebar
import components.main_body as components_body


# setting up default web UI setting
st.set_page_config(page_title="WhatToRead", layout="wide")

# init vars
components_body.init_vars()

render_header()
render_sidebar()


left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("Fill in at least one of the choices below")
    try:
        components_body.title_input()
        components_body.author_input()
        components_body.genre_selection()
        components_body.clear_genre_selection_button()
        components_body.recommend_books_button()
        components_body.display_recommendations()
    except Exception as e:
        st.error("ERROR!!!")
        st.exception(e)
    

with right_col:
    try:
        components_body.display_libraries()
    except Exception as e:
        st.error("ERROR!!!")
        st.exception(e)

    
