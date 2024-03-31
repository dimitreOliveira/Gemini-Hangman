import logging
import os

import streamlit as st
import torch
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import CATEGORIES, MAX_TRIES, configs
from hangman import guess_letter
from hf_utils import query_hint, query_word


@st.cache_resource()
def setup(model_id: str, device: str) -> None:
    """Initializes the model and tokenizer.

    Args:
        model_id (str): Model ID used to load the tokenizer and model.
    """
    logger.info(f"Loading model and tokenizer from model: '{model_id}'")
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=os.environ["HF_ACCESS_TOKEN"],
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        token=os.environ["HF_ACCESS_TOKEN"],
    ).to(device)
    logger.info("Setup finished")
    return {"tokenizer": tokenizer, "model": model}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

st.set_page_config(
    page_title="Gemini Hangman",
    page_icon="🧩",
)

load_dotenv()
assets = setup(configs["os_model"], configs["device"])

tokenizer = assets["tokenizer"]
model = assets["model"]

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
        model,
        tokenizer,
        configs["generation_config"],
        configs["device"],
    )
    st.session_state["hint"] = query_hint(
        st.session_state["word"],
        model,
        tokenizer,
        configs["generation_config"],
        configs["device"],
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
    ## Guess the word based on a hint
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
