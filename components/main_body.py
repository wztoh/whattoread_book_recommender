import streamlit as st
import uuid
import config
from utils.prompts import generate_system_prompt,generate_book_search_prompt,generate_format_recommendations_prompt
from utils.tavily_services import tavily_search,TavilySearchError
from utils.gemini_services import ask_gemini,GeminiServiceError
from utils.helper_functions import parse_recommendations
from utils.nlb_services import find_book_in_library

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

    # recommended book details
    if "recommended_books_list" not in st.session_state:
        st.session_state.recommended_books_list = []
    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None

def reset_session():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = [{"role": "system",
                                "content":generate_system_prompt()}]

    st.session_state.title_input = ""
    st.session_state.author_input = ""

    st.session_state.genre_pills = []
    st.session_state.genre_input_textfield = ""
    st.session_state.genre_combined = ""

    st.session_state.recommended_books_list = []
    st.session_state.selected_book = None

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
    try:
        tavily_result = tavily_search(user_criteria)
    except TavilySearchError as e:
        st.error("Tavily search errors.")
        st.exception(e)
    book_search_prompt = generate_book_search_prompt(user_criteria,tavily_result)


    # # store information to message history/session state before prompt
    st.session_state.messages.append({"role": "user",
                                      "content": user_criteria})

    
    # # get response from gemini
    # convert session_state.messages (list of dicts) into a hashable tuple for  st.cache
    hashable_history = tuple((m["role"], m["content"]) for m in st.session_state.messages)
    try:
        # response = ask_gemini(st.session_state.messages,book_search_prompt)
        response = ask_gemini(hashable_history,book_search_prompt)
    except GeminiServiceError as e:
        st.error("Gemini couldn't get book recommendations right now. Please try again.")
        st.exception(e)  

    try:
        if response in config.ERROR_MSG:
            st.warning(f"CODE:{response}. {config.ERROR_MSG[response]}")
    except Exception as e:
        st.warning(f"CODE {response}: {e}")

    # # store response to message history/session state after prompt
    st.session_state.messages.append({"role": "assistant",
                                     "content": response})

    try:
        format_prompt = generate_format_recommendations_prompt(response)
        formatted_response = ask_gemini([],format_prompt)

        formatted_response = parse_recommendations(formatted_response)
        st.session_state.recommended_books_list = formatted_response
    except GeminiServiceError as e:
        st.error("Gemini parsing result format into json failed.")
        st.exception(e)  
    except Exception as e:
        st.error("ERROR!!!")
        st.exception(e)


def recommend_books_button():
    if st.button("Recommend Books",
                 type="primary",
                 icon="📚"):
        st.session_state.selected_book = None # reset showing libraries
        recommend_books()

    
def display_recommendations():
    for i,book in enumerate(st.session_state.recommended_books_list):
        with st.container(border=True):
            st.subheader(book["title"])
            st.caption(book["author"])
            st.write(book["genre"])
            st.write(book["explanation"])
            if st.button("Check Availability", key=f"show_{i}"):
                try:
                    libraries = find_book_in_library(book["title"],book["author"])
                    st.session_state.recommended_books_list[i]["libraries"] = libraries
                    st.session_state.selected_book = i
                except Exception as e:
                    st.error("ERROR!!!")
                    st.exception(e)

def display_libraries():
    if st.session_state.selected_book != None:
        with st.container(border=True):
            try:
                book = st.session_state.recommended_books_list[st.session_state.selected_book]
                st.subheader(f"Libraries for {book['title']}")

                if "libraries" in book:
                    for lib in book["libraries"]:
                        st.success(f"• {lib}")
            except Exception as e:
                st.error("ERROR!!!")
                st.exception(e)