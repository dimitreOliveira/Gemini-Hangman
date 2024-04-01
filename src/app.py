import logging

import streamlit as st
import vertexai

from common import CATEGORIES, MAX_TRIES, configs
from hangman import guess_letter
from vertex_utils import query_hint, query_word


@st.cache_resource()
def setup(project: str, location: str) -> None:
    """Setups the Vertex AI project.

    Args:
        project (str): Vertex AI project name
        location (str): Vertex AI project location
    """
    vertexai.init(project=project, location=location)
    logger.info("Vertex AI setup finished")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

st.set_page_config(
    page_title="Gemini Hangman",
    page_icon="🧩",
)

setup(configs["project"], configs["location"])

if not st.session_state:
    st.session_state["word"] = ""
    st.session_state["hint"] = ""
    st.session_state["hangman"] = ""
    st.session_state["missed_letters"] = []
    st.session_state["correct_letters"] = []

st.title("Gemini Hangman")

st.markdown("## Guess the word based on a hint")

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox(
        "Choose a category",
        CATEGORIES,
    )

with col2:
    start_btn = st.button("Start game")
    reset_btn = st.button("Reset game")

if start_btn:
    st.session_state["word"] = query_word(
        category,
        configs["model"],
        configs["generation_config"],
    )
    st.session_state["hint"] = query_hint(
        st.session_state["word"],
        configs["model"],
        configs["generation_config"],
    )
    st.session_state["hangman"] = "_" * len(st.session_state["word"])
    st.session_state["missed_letters"] = []
    st.session_state["correct_letters"] = []

if reset_btn:
    st.session_state["word"] = ""
    st.session_state["hint"] = ""
    st.session_state["hangman"] = ""
    st.session_state["missed_letters"] = []
    st.session_state["correct_letters"] = []

st.markdown(
    """
    Note: you must input whitespaces and special characters.
    """
)

st.markdown(f'### Hint:\n{st.session_state["hint"]}')

col3, col4 = st.columns(2)

with col3:
    guess = st.text_input(label="Enter letter")
    guess_btn = st.button("Guess letter")

if guess_btn:
    st.session_state = guess_letter(guess, st.session_state)

with col4:
    hangman = st.text_input(
        label="Hangman",
        value=st.session_state["hangman"],
    )
    st.text_input(
        label=f"Missed letters (max  {MAX_TRIES} tries)",
        value=", ".join(st.session_state["missed_letters"]),
    )

if st.session_state["word"] == st.session_state["hangman"] != "":
    st.success("You won!")
    st.balloons()

if len(st.session_state["missed_letters"]) >= MAX_TRIES:
    st.error(f"""You lost, the correct word was '{st.session_state["word"]}'""")
    st.snow()
