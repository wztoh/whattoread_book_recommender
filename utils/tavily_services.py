from tavily import TavilyClient
import config
import streamlit as st

tavily_api_key = config.TAVILY_API_KEY

tavily_client = TavilyClient(api_key=tavily_api_key)

class TavilySearchError(Exception):
    """Raised when the Tavily search API call fails."""
    pass

def format_tavily_results(response_list, summary)->str:
    """
    Combine and format the results obtain from the web search
    Returns the result as a str
    """

    response_text = ""
    for i, response in enumerate(response_list,1):
        response_text = response_text + f"({i}) Title: {response["title"]} | Source: {response["source"]}\n{response["content"]}\n\n "

    formatted_text = f"""
High level summary from web results:
{summary}

Web results details:
{response_text}

"""
    return formatted_text


@st.cache_data(show_spinner="Searching web for similar books...")
def tavily_search(prompt:str, num_results:int=5)->str:
    """
    Calls Tavily Api to search the web.
    Returns a str that contains both Tavily LLM generated summary and content details it draws from
    """
    try:
        response = tavily_client.search(query=prompt, 
                                        max_results=num_results,
                                        include_answer="advanced")
        response_list = []

        for result in response["results"]:
            response_list.append({"title": result["title"],
                                "source":result["url"],
                                "content": result["content"][:400],
                                })

        formatted_result = format_tavily_results(response_list,response["answer"])
        return (formatted_result)
    
    except Exception as e:
        raise TavilySearchError(f"Tavily search failed: {e}") from e
