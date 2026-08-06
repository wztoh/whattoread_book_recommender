def generate_system_prompt()->str:
    system_prompt = """
You are a helpful and resourceful bot that functions like a digital librarian. Your user is a human who is looking for suggestions\
on books to read. Your role is to understand the user's search criteria, and give them book recommendations based on their preferences.\
You are supplied with additional search results from the web to aid you in selecting the books.
"""
    return system_prompt


def generate_book_search_prompt(user_criteria:str="",web_search_result:str="")->str:
    """
    LLM + web search RAG. Uses user input and web results to create a prompt to search for books recommendations.
    """

    prompt = f"""
Use the user criteria and additional web information to recommend books to the user.
    
User search criteria:
{user_criteria}


{web_search_result}



There are rules you must follow:
- you must not hallucinate or generate information for the book such as title or author if the information does not exist 
- do not attempt to rewrite the user's search terms, such as title, author or genre. Leave as verbatim.
- skip the book if previously it has been recommended to the user.


Present up to three book recommendations that best fit the criteria as a numbered list. Each recommendation must contain the book title, author, genre and explaination for choosing it.
If user criteria is empty, only output the exact word "400". Do not include punctuation, markdown, greetings, or explanations.
If there is no books that fufil the user's criteria, only output the exact word "404". Do not include punctuation, markdown, greetings, or explanations.


"""
    return prompt

def generate_format_recommendations_prompt(response:str):
    """
    Formats the result from book recommendations into a json format and returns it
    """
    
    prompt = f"""
You are given a text containing up to 3 book recommendations. Each recommendation includes a title, author, genre(s), and an explanation for why the book was recommended.

Extract the information for each book found in the text and format it as a JSON object with a single key "recommendations", whose value is a list of objects — one per book recommendation actually present in the text \
(this may be 1, 2, or 3; do not pad the list or invent extra entries to reach 3). Each object must have exactly these 4 keys:

- "title": string — the book's title
- "author": string — the author's full name
- "genre": string — the genre(s), as a single comma-separated string (e.g. "Science Fiction, Thriller")
- "explanation": string — the reason given for recommending the book

Rules:
- Output ONLY valid JSON. No preamble, no markdown code fences, no commentary.
- Include only recommendations that are actually present in the source text — never fabricate additional books to fill the list.
- Preserve the original wording of the explanation as closely as possible; do not add new information.
- If a field is missing or unclear for a given book, use an empty string "" for that field — do not omit the key or guess.
- Maintain the same order as the recommendations appear in the source text.
- If no book recommendations are found in the text, return {{"recommendations": []}}.

Text:
<text>
{response}
</text>

"""

    return prompt