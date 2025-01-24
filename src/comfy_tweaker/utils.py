import re


def match(text, pattern):
    """
    Filters a list to all the elements containing the pattern as a substring. Case insensitive.

    Args:
        text (list): The list of strings to filter.
        pattern (str): The substring pattern to match.

    Returns:
        list: A list of elements containing the pattern.
    """
    return [element for element in text if pattern.lower() in element.lower()]


def regex_match(text, pattern):
    """
    Filters a list to all the elements matching the regex pattern.

    Args:
        text (list): The list of strings to filter.
        pattern (str): The regex pattern to match.

    Returns:
        list: A list of elements matching the regex pattern.
    """
    return [element for element in text if re.match(pattern, element)]


def filter_collection(collection, match_, regex_match_):
    """
    Filters down a collection of files using the match and regex_match filters.

    Args:
        collection (list): The collection of files to filter.
        match (str): The substring pattern to match.
        regex_match (str): The regex pattern to match.

    Returns:
        list: The filtered collection of files.
    """
    if match_:
        collection = match(collection, match_)
    if regex_match_:
        collection = regex_match(collection, regex_match_)
    return collection
