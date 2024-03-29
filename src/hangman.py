import logging

from streamlit import session_state


def guess_letter(letter: str, session: session_state) -> session_state:
    """Take a letter and evaluate if it is part of the hangman puzzle
    then updates the session object accordingly.

    Args:Chosen letter
        letter (str): Streamlit session object
        session (session_state): _description_

    Returns:
        session_state: Updated session
    """
    logger.info(f"Letter {letter} picked")
    if letter in session["word"]:
        session["correct_letters"].append(letter)
    else:
        session["missed_letters"].append(letter)

    hangman = "".join(
        [
            (letter if letter in session["correct_letters"] else "_")
            for letter in session["word"]
        ]
    )
    session["hangman"] = hangman
    logger.info("Session state updated")
    return session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)
