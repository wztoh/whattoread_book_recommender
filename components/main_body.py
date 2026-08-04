import streamlit as st
import uuid
import config

def init_vars():
    """
    initialse all starting variables on new session
    """
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = [] #TODO pass in basic system prompt as first msg


    # genre selection    
    if "genre_pills" not in st.session_state:
        st.session_state.genre_pills = []
    if "genre_input_textfield" not in st.session_state:
        st.session_state.genre_input_textfield = ""    

def reset_session():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.genre_pills = []



def genre_pills_buttons():
    selected_genres = st.pills("Choose from the below genres. Type in the box if your genre is not listed.",
                                options=config.BOOK_GENRES_LIST,
                                selection_mode="multi",
                                key="genre_pills"
                                )
    return selected_genres

def genre_selection():
    try:
        selected_genres = genre_pills_buttons()
        genre_user_input = st.text_input("(Optional) Type your unlisted genre here",value="",key="genre_input_textfield")
        if genre_user_input != "":
            genre_user_input = f",{genre_user_input}"
        final_genre_selection = (",".join(selected_genres) + genre_user_input)

        st.info(f"Selected Genres: {final_genre_selection}")
    except Exception as e:
        st.error("ERROR!!!\n")
        st.exception(e)

def clear_genre_selection():
    st.session_state.genre_pills = []
    st.session_state.genre_input_textfield = ""

def clear_genre_selection_button():
    st.button(label="Clear all genre selection.", on_click=clear_genre_selection)

def title_input():
    return st.text_input("Title")

def author_input():
    return st.text_input("Author")
