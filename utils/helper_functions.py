import json


def parse_recommendations(llm_output: str) -> list[dict]:
    """
    Parse the JSON response from the book recommendation extraction prompt.
    Returns a list of book dicts, or an empty list if parsing fails.
    """
    # Strip markdown code fences if the model added them despite instructions
    cleaned = llm_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw output was: {llm_output!r}")
        return []

    return data.get("recommendations", [])