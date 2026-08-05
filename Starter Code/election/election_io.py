def read_electoral_votes(filename: str) -> dict[str, int]:
    """
    Processes the number of electoral votes for each state.
    Parameters:
    - filename (str): A filename string.
    Returns:
    - dict[str, int]: A dictionary that associates each state name (string)
      to an integer corresponding to its number of Electoral College votes.
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("filename must be a non-empty string.")

    pass

def read_polling_data(filename: str) -> dict[str, float]:
    """
    Parses polling percentages from a file.
    Parameters:
    - filename (str): A filename string.
    Returns:
    - dict[str, float]: A dictionary of state names (strings) to floats
      corresponding to the percentages for candidate 1.
    """

    if not filename or not isinstance(filename, str):
        raise ValueError("filename must be a non-empty string.")