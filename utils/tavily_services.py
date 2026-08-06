from tavily import TavilyClient
import config


tavily_api_key = config.TAVILY_API_KEY

tavily_client = TavilyClient(api_key=tavily_api_key)

def format_tavily_results(response_list, summary)->str:

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



def tavily_search(prompt:str, num_results:int=5)->str:
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

