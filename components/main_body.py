import streamlit as st
import uuid
import config
from utils.prompts import generate_system_prompt,generate_book_search_prompt
from utils.tavily_services import tavily_search
from utils.gemini_services import ask_gemini

def init_vars():
    """
    initialse all starting variables on new session
    """
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system",
                                      "content":generate_system_prompt()}]

    # user input
    if "title_input" not in st.session_state:
        st.session_state.title_input = ""
    if "author_input" not in st.session_state:
        st.session_state.author_input = ""

    # genre selection    
    if "genre_pills" not in st.session_state:
        st.session_state.genre_pills = []
    if "genre_input_textfield" not in st.session_state:
        st.session_state.genre_input_textfield = ""    
    if "genre_combined" not in st.session_state:
        st.session_state.genre_combined = ""

def reset_session():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = [{"role": "system",
                                "content":generate_system_prompt()}]

    st.session_state.title_input = ""
    st.session_state.author_input = ""

    st.session_state.genre_pills = []
    st.session_state.genre_input_textfield = ""
    st.session_state.genre_combined = ""

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
        # store into session var
        st.session_state.genre_combined = final_genre_selection
    except Exception as e:
        st.error("ERROR!!!\n")
        st.exception(e)

def clear_genre_selection():
    st.session_state.genre_pills = []
    st.session_state.genre_input_textfield = ""

def clear_genre_selection_button():
    st.button(label="Clear all genre selection.", on_click=clear_genre_selection)

def title_input():
    st.text_input("Title",key="title_input")

def author_input():
    st.text_input("Author",key="author_input")

def parse_user_criteria()->str:

    user_title = st.session_state.title_input
    user_author = st.session_state.author_input
    user_genre = st.session_state.genre_combined

    if user_title != "":
        user_title = f"titles similar to {user_title}."
    if user_author != "":
        user_author = f"works from {user_author}."
    if user_genre != "":
        user_genre = f"in genres like {user_genre}."
    
    parsed_text = f"""
Search for books with similar criteria:
{user_title}
{user_author}
{user_genre}
"""
    return parsed_text


def recommend_books():
    user_criteria = parse_user_criteria()
    tavily_result = tavily_search(user_criteria)
    book_search_prompt = generate_book_search_prompt(user_criteria)

    st.write(f"user critera: \n{user_criteria}")
    st.write(f"tavily result: \n{tavily_result}")
    st.write(f"book prompt:\n{book_search_prompt}")

    # # store information to message history/session state before prompt
    st.session_state.messages.append({"role": "user",
                                      "content": user_criteria})
    # # get response from gemini
    response = ask_gemini(st.session_state.messages,book_search_prompt)

    try:
        if response in config.ERROR_MSG:
            st.warning(f"CODE:{response}. {config.ERROR_MSG[response]}")
    except Exception as e:
        st.write(f"CODE {response}: {e}")

    # # store response to message history/session state after prompt
    st.session_state.messages.append({"role": "assistant",
                                     "content": response})


    st.write(f"BOOK RECOMMENDATION RESPONSE:\n{response}") #TODO remove once done

def recommend_books_button():
    if st.button("Recommend Books"):
        recommend_books()
    
