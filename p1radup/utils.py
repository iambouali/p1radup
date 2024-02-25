import validators
import unicodedata

def _is_free_of_control_characters(text):
    """
    Check if the given string is free of Unicode control characters.

    A control character is any character with a Unicode category of 'Cc'.
    These characters are typically non-printing and could affect the processing
    of text in various environments or applications.
    Full list: https://www.fileformat.info/info/unicode/category/Cc/list.htm

    Parameters:
    - text (str): The string to be checked.

    Returns:
    - bool: True if the string contains no Unicode control characters, False otherwise.
    """
    return all(unicodedata.category(c) != 'Cc' for c in text)


def is_url_valid(new_url):
    """
    Validates the given URL by checking for Unicode control characters and validating its format.

    This function first checks if the input string is free of Unicode control characters using the unicodedata.category method. 
    If it contains control characters, the function prints a message indicating that binary data is being ignored, 
    and returns False. If no control characters are found, it proceeds to check if the string is a valid URL using 
    the validators.url function. If the URL is not valid, it prints a message indicating that an invalid URL is being ignored, 
    and returns False. The function returns True only if the input passes both checks.

    Parameters:
    - new_url (str): The string to be validated as a URL.

    Returns:
    - bool: True if the input is a valid URL and free of Unicode control characters, False otherwise.
    """

    if not _is_free_of_control_characters(new_url):
        print(f"Ignoring binary data: {new_url}")
        return False
    if not validators.url(new_url):
        print(f"Ignoring invalid URL: {new_url}")
        return False
    return True
