import json


def save_file(filename="saved_cover_letter.txt", content=""):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def read_file(filename=""):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def response_to_json(response):
    """
    Parses a response from the ollama API into a list.

    Args:
        response (str): The response from the ollama API.

    Returns:
        list[dict] | None: A list of objects, or None if parsing fails.
    """
    parsed_response = clean_response(response)
    if not parsed_response:
        return None
    try:
        return json.loads(parsed_response)
    except json.JSONDecodeError:

        return None


def clean_response(response):
    """
    Given a string response from the ollama API, strip out the JSON block and decode it.

    Returns:
        str: The decoded JSON string, or None if there was an error parsing the JSON.
    """
    try:
        cleaned_response = (
            response.replace("```json", "").replace("```", "").replace("'", '"').strip()
        )

        return cleaned_response

    except (IndexError, json.JSONDecodeError) as e:
        print(f"[clean_response]\tError cleaning response: {e}")

        return None
