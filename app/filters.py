def truncate_words(text, word_limit=10):
    """
    Truncate the text to a certain number of words.
    
    :param text: The text to be truncated.
    :param word_limit: Maximum number of words to show.
    :return: Truncated text with ellipsis if needed.
    """
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + " "
    return text