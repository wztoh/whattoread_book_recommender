import streamlit as st
import config
import uuid

from components.header import render_header
from components.sidebar import render_sidebar
import components.main_body as components_body



# setting up default web UI
st.set_page_config(page_title="WhatToRead", layout="wide")

# init vars
components_body.init_vars()

render_header()
render_sidebar()




left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("Fill in at least one of the choices below")
    components_body.title_input()
    components_body.author_input()
    components_body.genre_selection()
    components_body.clear_genre_selection_button()
    components_body.recommend_books_button()
    

with right_col:
    st.info("right side testing") 

 #TODO
# main body code
# testing code (to remove)

st.write("st messages list", st.session_state.messages)
st.write("title input",st.session_state.title_input)
st.write("author_input",st.session_state.author_input)
st.write("genre_pills",st.session_state.genre_pills)
st.write("genre_input_textfield",st.session_state.genre_input_textfield)


#remove testing code
# st.write(st.session_state.session_id)
# if input := st.text_input("Write here"):
#     st.write(input)
# st.write("session genre_pills: ",st.session_state.genre_pills)

# st.write(f"title:{a}, author:{b}")

