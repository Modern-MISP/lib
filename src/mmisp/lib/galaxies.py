import json


def json_or_original_string(s: str) -> str | dict | list:
    try:
        return json.loads(s)
    except json.decoder.JSONDecodeError:
        return s


def parse_galaxy_authors(str_authors: str) -> list[str]:
    parsed_author = json_or_original_string(str_authors)
    if isinstance(parsed_author, str):
        parsed_author = [parsed_author]  # force to be a list
    assert isinstance(parsed_author, list)

    return parsed_author
