import time
from collections import deque
import requests
import config
from difflib import SequenceMatcher
import streamlit as st

API_KEY = config.NLB_API_KEY
APP_CODE = config.NLB_APP_CODE

BASE_URL = "https://openweb.nlb.gov.sg/api/v2/Catalogue"

HEADERS = {
    "X-API-Key": API_KEY,
    "X-App-Code": APP_CODE,
    "Accept": "application/json",
}

def get_with_retry(url, headers, params, retries=5):
    for attempt in range(retries):
        rate_limiter.wait()

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20,
        )

        if response.status_code != 429:
            response.raise_for_status()
            return response

        # Retry-After header if present
        retry_after = response.headers.get("Retry-After")

        if retry_after is not None:
            sleep = int(retry_after)
        else:
            sleep = 60

        print(f"Rate limited. Sleeping {sleep} seconds...")

        time.sleep(sleep)

    raise Exception("Exceeded maximum retries")


class NLBRateLimiter:
    """Enforce NLB limits:
        - max 1 request / second
        - max 15 requests / minute
    """

    def __init__(self):
        self.calls = deque()
        self.last_call = 0

    def wait(self):
        now = time.time()

        # 1 request / second
        elapsed = now - self.last_call
        if elapsed < 1.5:
            time.sleep(1.5 - elapsed)

        now = time.time()

        # remove calls older than 60 seconds
        while self.calls and now - self.calls[0] >= 60:
            self.calls.popleft()

        # max 15 calls / minute
        if len(self.calls) >= 15:
            sleep = 60 - (now - self.calls[0])
            if sleep > 0:
                time.sleep(sleep)

            now = time.time()

            while self.calls and now - self.calls[0] >= 60:
                self.calls.popleft()

        self.calls.append(time.time())
        self.last_call = time.time()


rate_limiter = NLBRateLimiter()


@st.cache_data(show_spinner="Searching for libraries...")
def get_availability(brn):
    """
    Searchs for libraries that have the book available
    Returns the JSON from GetAvailabilityInfo.
    """

    rate_limiter.wait()

    r = requests.get(
        f"{BASE_URL}/GetAvailabilityInfo",
        headers=HEADERS,
        params={"BRN": brn},
        timeout=20,
    )

    r.raise_for_status()

    return r.json()

@st.cache_data(show_spinner="Searching book from database...")
def search_book(title: str = "", author: str = "", limit: int = 20):
    """Returns only physical books."""

    rate_limiter.wait()

    params = {"Limit": limit}

    if title:
        params["Title"] = title

    if author:
        params["Author"] = author

    r = requests.get(
        f"{BASE_URL}/GetTitles",
        headers=HEADERS,
        params=params,
        timeout=20,
    )

    r.raise_for_status()

    data = r.json()

    # Keep only physical books
    books = [
        book
        for book in data.get("titles", [])
        if book.get("format", {}).get("name") == "Book"
    ]

    return books


def search_book_SearchTitles(title: str = "", author: str = "", limit: int = 20):
    """
    Search for books using SearchTitles and return only physical books.
    """

    rate_limiter.wait()

    # Build a keyword query
    # keywords = " ".join(filter(None, [title, author]))
    keywords = f"{title} {author}".strip()

    params = {
        "Keywords": keywords,
        "Limit": limit,
        "Offset": 0
    }

    r = requests.get(
        f"{BASE_URL}/SearchTitles",
        headers=HEADERS,
        params=params,
        timeout=20,
    )

    r.raise_for_status()

    data = r.json()

    # Keep only normal physical books
    books = [
        book
        for book in data.get("titles", [])
        if book.get("format", {}).get("name") == "Book"
    ]

    return books



def best_physical_book(title: str, books: list):
    """
    Return the physical book whose title best matches the requested title.
    Helps with controlling rate limit
    Cons is might exclude other book with different metadata
    """

    if not books:
        return None

    return max(
        books,
        key=lambda b: SequenceMatcher(
            None,
            title.lower(),
            b["title"].lower()
        ).ratio()
    )

def parse_available_libraries(availability_json):
    """
    Extract libraries that currently have a physical book
    available (including books that are currently being shelved).

    Returns
    -------
    list[str]
        Sorted list of unique library names.
    """

    libraries = set()

    for item in availability_json.get("items", []):

        if item.get("media", {}).get("name") != "Book":
            continue

        key = (
            item.get("status", {}).get("code"),
            item.get("transactionStatus", {}).get("code"),
        )

        if key in AVAILABLE_STATUS:
            libraries.add(item["location"]["name"])

    return sorted(libraries)

AVAILABLE_STATUS = {
    ("Shelving", "S"),      # Recently returned
    ("Available", "S"),     # If NLB uses this status
}



def find_book_in_library(title:str="",author:str=""):
    """
    Uses NLB Api to find libraries that has available physical book
    Returns the list of library names with book availabilty
    """

    books = search_book(title, author)

    # Pick the best matching physical edition (control limit rate)
    book = best_physical_book(title, books)

    # # no book is found
    if book is None:
        return []

    # Query library availability
    availability = get_availability(book["brn"])

    lib  =  parse_available_libraries(availability)

    return lib


    