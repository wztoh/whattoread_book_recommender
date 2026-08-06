import os
from dotenv import load_dotenv


load_dotenv()

# retrive keys from local environment variables
MODEL =  os.getenv("MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NLB_API_KEY = os.getenv("NLB_API_KEY")
NLB_APP_CODE = os.getenv("NLB_APP_CODE")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

BOOK_GENRES_LIST = [
    "fantasy",
    "science fiction",
    "romance",
    "mystery",
    "thriller and suspense",
    "horror",
    "history",
    "self-help",
    "crime"
]


ERROR_MSG = {"400": "Request failed. Fill in at least one search criteria.",
             "404": "Search request failed."}


